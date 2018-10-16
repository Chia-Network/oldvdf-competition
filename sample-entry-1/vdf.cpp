/**
Copyright 2018 Chia Network Inc

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
**/

#include <iostream>
#include <gmpxx.h>

using namespace std;

struct form {
    // y = ax^2 + bxy + y^2
    mpz_t a;
    mpz_t b;
    mpz_t c;

    mpz_t d; // discriminant
};

ostream& operator<<(ostream& os, const form& f) {
    return os << "a: " <<  f.a << endl << "b: " << f.b << endl << "c: " << f.c << endl;
}

void normalize(form& f) {
    mpz_t negative_a;
    mpz_init(negative_a);
    mpz_neg(negative_a, f.a);
    if (mpz_cmp(f.b, negative_a) > 0 && mpz_cmp(f.b, f.a) <= 0) {
        // Already normalized
        return;
    }
    // r = (a - b) / 2a
    // a = a
    // b = b + 2ra
    // c = ar^2 + br + c
    mpz_t r;
    mpz_init_set(r, f.a);
    mpz_sub(r, r, f.b);

    mpz_t denom;
    mpz_init_set(denom, f.a);
    mpz_mul_ui(denom, denom, 2);

    // r = (a-b) / 2a
    mpz_fdiv_q(r, r, denom);

    mpz_t old_b;
    mpz_init_set(old_b, f.b);

    mpz_t ra;
    mpz_init_set(ra, r);
    mpz_mul(ra, ra, f.a);
    mpz_add(f.b, f.b, ra);
    mpz_add(f.b, f.b, ra);

    // c += ar^2
    mpz_mul(ra, ra, r);
    mpz_add(f.c, f.c, ra);

    // c += rb
    mpz_set(ra, r);
    mpz_mul(ra, ra, old_b);
    mpz_add(f.c, f.c, ra);
}

void reduce(form& f) {
    normalize(f);
    while ((mpz_cmp(f.a, f.c) > 0) ||
           (mpz_cmp(f.a, f.c) == 0 && mpz_cmp_si(f.b, 0) < 0)) {
        mpz_t s;
        mpz_init_set(s, f.c);
        mpz_add(s, s, f.b);

        // x = 2c
        mpz_t x;
        mpz_init_set(x, f.c);
        mpz_mul_ui(x, x, 2);
        mpz_fdiv_q(s, s, x);

        mpz_t old_a;
        mpz_t old_b;
        mpz_init_set(old_a, f.a);
        mpz_init_set(old_b, f.b);

        // b = -b
        mpz_set(f.a, f.c);
        mpz_neg(f.b, f.b);

        // x = 2sc
        mpz_set(x, s);
        mpz_mul(x, x, f.c);
        mpz_mul_ui(x, x, 2);

        // b += 2sc
        mpz_add(f.b, f.b, x);

        // c = cs^2
        mpz_mul(f.c, f.c, s);
        mpz_mul(f.c, f.c, s);

        // x = bs
        mpz_set(x, old_b);
        mpz_mul(x, x, s);

        // c -= bs
        mpz_sub(f.c, f.c, x);

        // c += a
        mpz_add(f.c, f.c, old_a);
    }
    normalize(f);
}

form generator_for_discriminant(mpz_t* d) {
    form x;
    mpz_init_set_ui(x.a, 2);
    mpz_init_set_ui(x.b, 1);
    mpz_init(x.c);
    mpz_init_set(x.d, *d);

    // c = b*b - d
    mpz_mul(x.c, x.b, x.b);
    mpz_sub(x.c, x.c, x.d);

    // denom = 4a
    mpz_t denom;
    mpz_init(denom);
    mpz_mul_ui(denom, x.a, 4);

    mpz_fdiv_q(x.c, x.c, denom);
    reduce(x);
    return x;
}

// Takes the gcd of three numbers
void three_gcd(mpz_t& ret, mpz_t& a, mpz_t& b, mpz_t& c) {
    mpz_gcd(ret, a, b);
    mpz_gcd(ret, ret, c);
}

// Returns mu and v, solving for x:  ax = b mod m
// such that x = u + vn (n are all integers). Assumes that mu and v are initialized.
// Returns 0 on success, -1 on failure
int solve_linear_congruence(mpz_t& mu, mpz_t& v, mpz_t& a, mpz_t& b, mpz_t& m) {
    mpz_t g, d, e;
    mpz_init(g);
    mpz_init(d);
    mpz_init(e);

    // g = gcd(a, m), and da + em = g
    mpz_gcdext(g, d, e, a, m);

    // q = b/g, r = b % g
    mpz_t q, r;
    mpz_init(q);
    mpz_init(r);
    mpz_fdiv_qr(q, r, b, g);

    if (mpz_cmp_ui(r, 0) != 0) {
        // No solution, return error. Optimize out for speed..
        cout << "No solution to congruence" << endl;
        return -1;
    }

    mpz_mul(mu, q, d);
    mpz_mod(mu, mu, m);

    mpz_fdiv_q(v, m, g);
    return 0;
}

form multiply(form &f1, form &f2) {
    assert(mpz_cmp(f1.d, f2.d) == 0);

    // g = (b1 + b2) / 2
    mpz_t g;
    mpz_init(g);
    mpz_add(g, f1.b, f2.b);
    mpz_fdiv_q_ui(g, g, 2);


    // h = (b2 - b1) / 2
    mpz_t h;
    mpz_init(h);
    mpz_sub(h, f2.b, f1.b);
    mpz_fdiv_q_ui(h, h, 2);

    // w = gcd(a1, a2, g)
    mpz_t w;
    mpz_init(w);
    three_gcd(w, f1.a, f2.a, g);

    // j = w
    mpz_t j;
    mpz_init_set(j, w);

    // r = 0
    mpz_t r;
    mpz_init_set_ui(r, 0);

    // s = a1/w
    mpz_t s;
    mpz_init(s);
    mpz_fdiv_q(s, f1.a, w);

    // t = a2/w
    mpz_t t;
    mpz_init(t);
    mpz_fdiv_q(t, f2.a, w);

    // u = g/w
    mpz_t u;
    mpz_init(u);
    mpz_fdiv_q(u, g, w);

    // solve (tu)k = (hu + sc1) mod st, of the form k = mu + vn
    mpz_t a, b, m; // Used for solving equation

    // a = tu
    mpz_init(a);
    mpz_mul(a, t, u);

    // b = hu + sc1
    mpz_init(b);
    mpz_mul(b, h, u);
    mpz_init(m); // Use m as a temp variable
    mpz_mul(m, s, f1.c);
    mpz_add(b, b, m);

    // m = st
    mpz_mul(m, s, t);

    mpz_t mu, v; // solutions to equation
    mpz_init(mu);
    mpz_init(v);
    int ret = solve_linear_congruence(mu, v, a, b, m);

    assert(ret == 0);

    // solve (tv)n = (h - t * mu) mod s, of the form n = lamda + sigma n'

    // a = tv
    mpz_mul(a, t, v);

    // b = h - t * mu
    mpz_mul(m, t, mu); // use m as a temp variable
    mpz_sub(b, h, m);

    // m = s
    mpz_set(m, s);

    mpz_t lambda, sigma; // solutions to equation
    mpz_init(lambda);
    mpz_init(sigma);

    ret = solve_linear_congruence(lambda, sigma, a, b, m);
    assert(ret == 0);

    // k = mu + v*lamda
    mpz_mul(a, v, lambda); // use a as a temp variable

    mpz_t k;
    mpz_init(k);
    mpz_add(k, mu, a);

    // l = (k*t - h) / s
    mpz_t l;
    mpz_init(l);
    mpz_mul(l, k, t);
    mpz_sub(l, l, h);
    mpz_fdiv_q(l, l, s);

    // m = (tuk - hu - cs) / st
    mpz_mul(m, t, u);
    mpz_mul(m, m, k);
    mpz_mul(a, h, u); // use a as a temp variable
    mpz_sub(m, m, a);
    mpz_mul(a, f1.c, s); // use a as a temp variable
    mpz_sub(m, m, a);
    mpz_mul(a, s, t); // use a as a temp variable
    mpz_fdiv_q(m, m, a);

    form f3;

    // A = st - ru
    mpz_init(f3.a);
    mpz_mul(f3.a, s, t);
    mpz_mul(a, r, u); // use a as a temp variable
    mpz_sub(f3.a, f3.a, a);

    // B = ju + mr - (kt + ls)
    mpz_init(f3.b);
    mpz_mul(f3.b, j, u);
    mpz_mul(a, m, r); // use a as a temp variable
    mpz_add(f3.b, f3.b, a);
    mpz_mul(a, k, t); // use a as a temp variable
    mpz_sub(f3.b, f3.b, a);
    mpz_mul(a, l, s); // use a as a temp variable
    mpz_sub(f3.b, f3.b, a);

    // C = kl - jm
    mpz_init(f3.c);
    mpz_mul(f3.c, k, l);
    mpz_mul(a, j, m);
    mpz_sub(f3.c, f3.c, a);

    mpz_init_set(f3.d, f1.d);

    reduce(f3);
    return f3;
}

// Performs the VDF squaring iterations
form repeated_square(form f, uint64_t iterations) {
    for (uint64_t i=0; i < iterations; i++) {
        f = multiply(f, f);
    }
    return f;
}

int main(int argc, char* argv[]) {
    mpz_t discriminant;
    int ret = mpz_init_set_str(discriminant, argv[1], 0);
    uint64_t iterations = stoi(argv[2]);
    assert(ret == 0);
    form x = generator_for_discriminant(&discriminant);
    form y = repeated_square(x, iterations);

    // Outputs a and b of final element
    cout << y.a << endl << y.b;
}
