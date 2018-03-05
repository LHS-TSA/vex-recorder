/**
 * ###################################################
 * ### DO NOT EDIT --- THIS CODE IS AUTO GENERATED ###
 * ###################################################
 *
 * This file's data was recorded on:
 *  - 2018-03-02T18:42:54Z
 *
 * Author(s):
 *  - Stephen DuVall (@stphnduvall)
 *  - John Hancock (@jhnhnck)
 */

#include "API.h"
#include "constants.h"
#include "motors.h"

void auton_1520016174(Encoder le, Encode re) {
  /**
   *  ______     ______     ______     ______     __  __     ______   ______     __     __   __     ______
   * /\  == \   /\  == \   /\  ___\   /\  __ \   /\ \/ /    /\  == \ /\  __ \   /\ \   /\ "-.\ \   /\__  _\
   * \ \  __<   \ \  __<   \ \  __\   \ \  __ \  \ \  _"-.  \ \  _-/ \ \ \/\ \  \ \ \  \ \ \-.  \  \/_/\ \/
   *  \ \_____\  \ \_\ \_\  \ \_____\  \ \_\ \_\  \ \_\ \_\  \ \_\    \ \_____\  \ \_\  \ \_\\"\_\    \ \_\
   *   \/_____/   \/_/ /_/   \/_____/   \/_/\/_/   \/_/\/_/   \/_/     \/_____/   \/_/   \/_/ \/_/     \/_/
   *
   */

  // 0 [0, 0, 0, 0, 0, 0] [0, 0, 257, 870]
  setVelocityRoller(0);
  doMotorTick();
  delay(AUTON_LOOP_DELAY);

  // Condenensed 769 empty cycles
  doMotorTick();
  delay(AUTON_LOOP_DELAY * 769);
}
