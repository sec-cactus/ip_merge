# -*- coding:utf-8-
import sys

ip_number_repeat = []
ip_number_merge = []


def is_valid_ip(ip):
    ip_list = ip.split('.')
    if ip is None or ip == '':
        print 'Invalid IP: None'
        return False
    if len(ip_list) < 4:
        print 'Invalid IP:', ip
        return False
    for i in ip_list:
        if not i.isdigit():
            print 'Invalid IP:', ip
            return False
        elif int(i) < 0 or int(i) > 255:
            print 'Invalid IP:', ip
            return False
    return True
    pass


def ip_to_number(ip):
    if not is_valid_ip(ip):
        return -1

    ip_list = ip.strip().split('.')

    ip_number = int(ip_list[0]) * 256 * 256 * 256
    ip_number = int(ip_list[1]) * 256 * 256 + ip_number
    ip_number = int(ip_list[2]) * 256 + ip_number
    ip_number = int(ip_list[3]) + ip_number
    return ip_number
    pass


def number_to_ip(number):
    ip_list = ''

    ip_list = ip_list + str((number / 256 / 256 / 256) % 256) + '.'
    ip_list = ip_list + str((number / 256 / 256) % 256) + '.'
    ip_list = ip_list + str((number / 256) % 256) + '.'
    ip_list = ip_list + str(number % 256)

    return ip_list
    pass


def number_to_list(number):
    if ip_number_merge.__contains__(number):
        if not ip_number_repeat.__contains__(number):
            ip_number_repeat.append(number)
    else:
        ip_number_merge.append(number)
    pass


def mask_to_ip(line):
    l = line.split('/')
    ip_head = l[0]
    mask = int(l[1])

    ip_number = ip_to_number(ip_head)
    if ip_number < 0:
        return

    if mask < 0 or mask > 32:
        print 'Invalid mask:', mask
        return

    mask_number = 0
    for m in range((32-mask), 32):
        mask_number = mask_number + (2 ** m)

    start = ip_number & mask_number
    end = start + 2 ** (32 - mask)
    for ip_number in range(start + 1, end - 1): #start:networkID, end:broadcast
        number_to_list(ip_number)

    pass


def part_to_ip(line):
    l = line.split('-')
    start = ip_to_number(l[0])
    end = ip_to_number(l[1])

    if start < 0 or end < 0:
        return

    for ip_number in range(start, (end + 1)):
        number_to_list(ip_number)

    pass


def list_to_part(ip_map):
    ip_map.sort()
    start = -1
    ip_part = []

    for i in range(0, len(ip_map)):
        if i == 0:
            start = i

        if i == len(ip_map) - 1:
            end = i
            ip_part.append(number_to_ip(ip_map[start]) + '-' + number_to_ip(ip_map[end]))
            continue

        if ip_map[i + 1] - ip_map[i] > 1:
            end = i
            ip_part.append(number_to_ip(ip_map[start]) + '-' + number_to_ip(ip_map[end]))
            continue

        if 0 < i < (len(ip_map) - 1):
            if ip_map[i] - ip_map[i - 1] > 1:
                start = i
            if ip_map[i + 1] - ip_map[i] > 1:
                end = i
                ip_part.append(number_to_ip(ip_map[start]) + '-' + number_to_ip(ip_map[end]))
                continue

    return ip_part
    pass


if __name__ == '__main__':
    arg = sys.argv
    if len(arg) < 2:
        print "Usage: python run.py input_file"
        print "ip examples:"
        print "192.168.0.1"
        print "192.168.0.1/24"
        print "192.168.0.1-192.168.0.100"
        sys.exit(0)
    input_file = arg[1]

    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if len(line) < 1:
                continue

            if len(line.split('/')) > 1:
                print 'start process', line
                mask_to_ip(line)
            elif len(line.split('-')) > 1:
                print 'start process', line
                part_to_ip(line)
            else:
                print 'start process', line
                ip_number = ip_to_number(line)
                if not ip_number < 0:
                    number_to_list(ip_number)
                pass

    ip_merge = list_to_part(ip_number_merge)
    ip_repeat = list_to_part(ip_number_repeat)

    print 'merge:'
    for line in ip_merge:
        print line
    print 'repeat:'
    for line in ip_repeat:
        print line



    pass
