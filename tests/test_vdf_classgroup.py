import textwrap

from inkfish.classgroup import ClassGroup

from tests.common import exercise_code_verbosely


def classgroup_functions():
    discriminant = int(''.join(textwrap.dedent("""
        -277932370013051706986565094977558440925863868724962956297798375079711
        1755935469152358189047817691469335967563030108724222799555095874359204
        6124379271342523117944672201940224307563498623282396336043787901362415
        6433157943598984236289762294443851324618151831207090436519745445815231
        7564548579388388954361501155915180650886278614483121267374719433736283
        5767292592316842392285011597319847853278165631070684231627247677822273
        5939990747234338712430307680633635599311944191428099762576753484986313
        5593175689179199446755860152120839703879033915840019194533960922418362
        5935566879000287625158572127711542235803324639115306136663""").split("\n")))

    discriminant = -497333706520175843802401785845247633092951073654583682148673589759912972969047267665487

    initial_x = ClassGroup.from_ab_discriminant(2, 1, discriminant)

    # |b| <= |a| <= |c| which is approx half the bytes of the discriminant
    # c can be calculated from a and b, so we only need to send (a, b)
    element_size_bytes = discriminant.bit_length() // 8
    return (initial_x, initial_x.identity(), element_size_bytes,
            int(discriminant.bit_length()))


def test_main():
    exercise_code_verbosely(classgroup_functions)


if __name__ == '__main__':
    test_main()


"""
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
"""
