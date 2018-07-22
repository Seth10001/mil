from txros import util
from mil_misc_tools import text_effects

SPEED_LIMIT = 0.15  # m/s

fprint = text_effects.FprintFactory(title="STRIPPER", msg_color="cyan").fprint


@util.cancellableInlineCallbacks
def pitch(sub):
    start = sub.move.forward(0).zero_roll_and_pitch()
    pitches = [start.pitch_down_deg(7), start] * 5
    for p in pitches:
        yield p.go(speed=0.1)


@util.cancellableInlineCallbacks
def run(sub):
    fprint('Starting...')
    sub_start_position, sub_start_orientation = yield sub.tx_pose()
    fprint(sub_start_orientation)
    yield sub.nh.sleep(5)

    sub_start = sub.move.forward(0).zero_roll_and_pitch()
    yield sub_start.down(1).set_orientation(sub_start_orientation).go(
        speed=0.1)
    yield sub.nh.sleep(3)

    start = sub.move.forward(0).zero_roll_and_pitch()
    # fprint('Searching... pitching...')
    # yield pitch(sub)
    fprint('Moving to gate')
    gate = start.forward(3)
    yield gate.go(speed=SPEED_LIMIT)
    yield sub.nh.sleep(3)
    # fprint('Searching... pitching')
    # yield pitch(sub)
    fprint('Going right in front of pole')
    pole = gate.forward(8.7)
    yield pole.go(speed=SPEED_LIMIT)
    yield sub.nh.sleep(3)

    fprint('Going around pole')
    offset_left = 1.7
    offset_forward = 1.7

    pole_l = pole.left(offset_left)
    yield pole_l.go(speed=SPEED_LIMIT)
    yield sub.nh.sleep(3)

    pole_f = pole_l.forward(offset_forward)
    yield pole_f.go(speed=SPEED_LIMIT)
    yield sub.nh.sleep(3)

    pole_r = pole_f.right(offset_left * 2)
    yield pole_r.go(speed=SPEED_LIMIT)
    yield sub.nh.sleep(3)

    pole_b = pole_r.backward(offset_forward * 2)
    yield pole_b.go(speed=SPEED_LIMIT)
    yield sub.nh.sleep(3)

    yield pole.go(speed=SPEED_LIMIT)
    yield sub.nh.sleep(5)

    fprint('Turning back to gate')
    yield pole.backward(1).go(speed=SPEED_LIMIT)
    yield sub.nh.sleep(5)
    fprint('Look at gate')
    yield sub.move.look_at(gate._pose.position).go(speed=SPEED_LIMIT)
    yield sub.nh.sleep(5)
    fprint('Going to gate')
    yield gate.yaw_left_deg(180).go(speed=SPEED_LIMIT)
    yield sub.nh.sleep(5)
    fprint('Go past through gate')
    yield start.yaw_left_deg(180).go(speed=SPEED_LIMIT)
