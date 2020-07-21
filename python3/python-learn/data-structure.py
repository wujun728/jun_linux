''' find a pair of numbers that the sum is equal for asked in an sorted array
'''
def find_two_sum(data, sum):
    begin_pos = 0
    end_pos = len(data) - 1
    while begin_pos < end_pos:
        if (data[begin_pos] + data[end_pos]) > sum:
            end_pos -= 1
        elif (data[begin_pos] + data[end_pos]) < sum:
            begin_pos += 1
        else:
            print "FIND:[%d,%d]" % (data[begin_pos], data[end_pos])
            end_pos -= 1
            begin_pos += 1

def test_find_two():
    data = [0, 1, 2, 3, 5, 7, 9, 13, 14]
    find_two_sum(data, 8)

if __name__ == '__main__':
    test_find_two()
