#!/usr/bin/python

# Control script for audio relays: turn specified channels on and others off.
#
# Copyright (C) 2013-2014 David Liu (http://iceboundflame.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import RPi.GPIO as GPIO
import time

PIN_MAP = { 	0:[11, 7],
		1:[12, 13],
		2:[15, 16],
		3:[22, 18],
		'z':[24, 26] }	# Impedance Matching

NUM_ROOMS = len(PIN_MAP)-1
PULSE_TIME = 0.050 # seconds

def pulse_relay_pin(pin):
	print "Pulsing IO pin",pin
	GPIO.output(pin, GPIO.HIGH)
	time.sleep(PULSE_TIME)
	GPIO.output(pin, GPIO.LOW)
	time.sleep(PULSE_TIME/2)

#
# Parse input parameters into onoff_map (list of 0/1=off/on for each room)
#

onoff_map = [0] * NUM_ROOMS
NUM_ROOMS_ON = len(sys.argv[1:])
for room in sys.argv[1:]:
	room = int(room)
	assert room >= 0 and room < NUM_ROOMS
	onoff_map[room] = 1


#
# input validated, now pulse pins
#

GPIO.setmode(GPIO.BOARD)
for group in PIN_MAP.values():
	for pin in group:
		GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)
	# initialize all the pins low.
	# this is OKAY because all relay *coils* will be off,
	# and nothing will switch until the pulses are initiated.

# enable impedance protection, unless exactly one pair of speakers is in use
if NUM_ROOMS_ON != 1:
	pulse_relay_pin(PIN_MAP['z'][1])

# toggle coils sequentially, one at a time (to limit current draw)
for room, onoff in enumerate(onoff_map):
	sel_pin = PIN_MAP[room][onoff]
	pulse_relay_pin(sel_pin)

# enable "single pair direct" if exactly one pair of speakers is in use
if NUM_ROOMS_ON == 1:
        pulse_relay_pin(PIN_MAP['z'][0])

GPIO.cleanup()
