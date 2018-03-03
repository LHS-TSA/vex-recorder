import json
import os
from datetime import datetime

template_before = """\
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

#include "constants.h"
#include "motors.h"
#include "API.h"

void auton_{}(Encoder le, Encode re) {{
"""

template_line ="""\
  // {} {} {}
  setVelocityLY({});
  setVelocityRY({});
  setVelocityDR4B({});
  setVelocityMogo({});
  setVelocityFourBar({});
  setVelocityRoller({});

  doMotorTick();
  delay(AUTON_LOOP_DELAY);

"""

template_after = '}'


def generate_file(basename):
  in_filename = 'recordings/{}.txt'.format(basename)
  out_filename = 'src/{}_generated.c'.format(basename)
  record_date = basename

  if record_date.isnumeric():
    record_date = datetime.utcfromtimestamp(int(basename)).strftime('%Y-%m-%dT%H:%M:%SZ')

  with open(in_filename) as in_file:
    with open(out_filename, 'w') as out_file:
      out_file.write(template_before.format(
        record_date,
        basename))
      for line in in_file:
        try:
          packet = json.loads(line)
          for key, value in packet.items():
            out_file.write(template_line.format(key, value[0], value[1], *(value[0])))
        except Exception as e:
          print ('Error on Line {}: {}\n{}'.format(out_file.tell(), e, line))
      out_file.write(template_after)


if __name__ == "__main__":
  for filename in os.listdir('./recordings/'):
    basename = filename.split('.')[0]
    print('recordings/{}.txt => src/{}_generated.c'.format(basename, basename))
    generate_file(basename)
