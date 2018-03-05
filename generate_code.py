import json
import os
from datetime import datetime

template = {
  'before': """\
/**
 * ###################################################
 * ### DO NOT EDIT --- THIS CODE IS AUTO GENERATED ###
 * ###################################################
 *
 * This file's data was recorded on:
 *  - {}
 *
 * Author(s):
 *  - Stephen DuVall (@stphnduvall)
 *  - John Hancock (@jhnhnck)
 */

#include "API.h"
#include "constants.h"
#include "motors.h"

void auton_{}(Encoder le, Encode re) {{""",
  'breakpoint': [
    '\n  /**',
    '   *  ______     ______     ______     ______     __  __     ______   ______     __     __   __     ______',
    '   * /\  == \   /\  == \   /\  ___\   /\  __ \   /\ \/ /    /\  == \ /\  __ \   /\ \   /\ "-.\ \   /\__  _\\',
    '   * \ \  __<   \ \  __<   \ \  __\   \ \  __ \  \ \  _"-.  \ \  _-/ \ \ \/\ \  \ \ \  \ \ \-.  \  \/_/\ \/',
    '   *  \ \_____\  \ \_\ \_\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_\    \ \_____\  \ \_\  \ \_\\\\"\_\    \ \_\\',
    '   *   \/_____/   \/_/ /_/   \/_____/   \/_/\/_/   \/_/\/_/   \/_/     \/_____/   \/_/   \/_/ \/_/     \/_/',
    '   *',
    '   */',
  ],
  'comment': '\n  // {} {} {}',
  'functions': [
    '  setVelocityLY({});',
    '  setVelocityRY({});',
    '  setVelocityDR4B({});',
    '  setVelocityMogo({});',
    '  setVelocityFourBar({});',
    '  setVelocityRoller({});',
  ],
  'section_end': [
    '  doMotorTick();',
    '  delay(AUTON_LOOP_DELAY);',
  ],
  'section_delay': [
    '\n  // Condenensed {} empty cycles',
    '  doMotorTick();',
    '  delay(AUTON_LOOP_DELAY * {});',
  ],
  'section_delay_end': [
    '\n  // Recording ended with {} empty cycles (Line added below if needed)',
    '  // delay(AUTON_LOOP_DELAY * {});',
  ],
  'after': '}\n'
}

speed_defaults = [0, 0, 0, 0, 0, 30]

def unpack(packet):
  for key, dataset in packet.items():
    if len(dataset[0]) != 6:
      raise Exception('Invalid array length for speeds: {}',format(dataset[0]))

    if len(dataset[1]) != 4:
      raise Exception('Invalid array length for sensors:  {}',format(dataset[1]))

    return key, dataset[0], dataset[1]


def generate_file(basename):
  in_filename = 'recordings/{}.txt'.format(basename)
  out_filename = 'src/{}_generated.c'.format(basename)
  record_date = basename

  if record_date.isnumeric():
    record_date = datetime.utcfromtimestamp(int(basename)).strftime('%Y-%m-%dT%H:%M:%SZ')

  with open(in_filename) as in_file:
    with open(out_filename, 'w') as out_file:
      zero_count = 0

      out_file.write(template.get('before').format(record_date, basename))

      for line in in_file:
        try:
          packet = json.loads(line)

          if packet.get('break', False):
            for line in template.get('breakpoint'):
              out_file.write('{}\n'.format(line))
            continue

          cycle, speed_set, sensor_set = unpack(packet)
          setters = []
          write_lines = []

          for i in range(0, 6):
            if speed_set[i] != speed_defaults[i]:
              setters.append(template.get('functions')[i].format(speed_set[i]))


          if len(setters) != 0:
            if zero_count > 0:
              for line in template.get('section_delay'):
                write_lines.append(line.format(zero_count))

            write_lines.append(template.get('comment').format(cycle, speed_set, sensor_set))
            write_lines.extend(setters)
            write_lines.extend(template.get('section_end'))

            zero_count = 0
          else:
            zero_count += 1

          for line in write_lines:
            out_file.write('{}\n'.format(line))

        except Exception as e:
          print('Error on Line {}: {}\n{}'.format(out_file.tell(), e, line))
          continue


      if zero_count > 0:
        for line in template.get('section_delay'):
          out_file.write('{}\n'.format(line.format(zero_count)))

      out_file.write(template.get('after'))


if __name__ == "__main__":
  for filename in os.listdir('./recordings/'):
    basename = filename.split('.')[0]
    print('recordings/{}.txt => src/{}_generated.c'.format(basename, basename))
    generate_file(basename)
