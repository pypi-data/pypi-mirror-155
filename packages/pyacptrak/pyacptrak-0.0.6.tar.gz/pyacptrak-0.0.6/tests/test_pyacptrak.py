from pyacptrak import *
import pytest

#Test Segment
def test_seg_input():
	with pytest.raises(Exception) as e_info:
		Segment(2)

def test_seg_plot_1():
	with pytest.raises(Exception) as e_info:
		Segment('aa').plot('a')

def test_seg_plot_2():
	assert isinstance(Segment('aa').plot(20), Segment)

def test_seg_add():
	assert isinstance((Segment('aa') + Segment('aa')), Track)

#Test Track
def test_track_input_seg():
	with pytest.raises(Exception) as e_info:
		Track([2,3])

def test_track_plot_1():
	with pytest.raises(Exception) as e_info:
		Track([Segment('aa'), Segment('ab')]).plot('a')

def test_track_plot_2():
	assert isinstance(TRACK180.plot(20), Track)

def test_track_add1():
	assert isinstance((Segment('aa') + TRACK180), Track)

def test_track_add2():
	assert isinstance((TRACK45 + TRACK45), Track)

#Test Loop
def test_loop_length_1():
	assert Loop().info()['length'] == 3240

def test_loop_length_2():
	assert Loop(3,3).info()['length'] == 7200

def test_loop_plot_1():
	with pytest.raises(Exception) as e_info:
		Loop(3,3).plot('a')

def test_loop_plot_2():
	assert isinstance(Loop(3,3).plot(20), Loop)

def test_loop_add1():
	assert isinstance((Loop(3,3) + Segment('aa')), Assembly)

def test_loop_add2():
	assert isinstance((Loop(3,3) + TRACK45), Assembly)

#Test Assembly





