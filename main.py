ip = []
first_ip = []
first_valid_ip = ""
first_subnet_end_ip = []
first_subnet_valid_end_ip = ""
differ_in_subnet = []
last_ip = []
last_valid_ip = ""
sub = []
subnet_slash = 0
given_subnet = 0
bin_ip = []
bin_sub = []
net_index = []
host_index = []
subnet_groups = []
finished = 0


def start():
    global ip, first_ip, first_valid_ip, first_subnet_end_ip, first_subnet_valid_end_ip, differ_in_subnet, last_ip, last_valid_ip, sub, subnet_slash, given_subnet, bin_ip, bin_sub, net_index, host_index, subnet_groups
    clear_variables()

    ip = input("Please Enter IP Address: ").split(".")

    if not is_valid(ip):
        print("Invalid IP, Try again!\n\n")
        return 0

    sub = input("Please Enter Subnet: ")

    if not is_valid_sub(sub):
        print("Invalid subnet, Try again!\n\n")
        return 0

    given_subnet = input("Please enter slash subnet to do subnetting: ")

    if not is_valid_given_sub(given_subnet):
        print("Invalid subnet, Try again!\n\n")
        return 0

    decToBinIP(ip.copy())
    tmp = bin_ip.copy()
    first_ip = calculateIP(tmp, net_index, 0)
    first_valid_ip = calculateIPDecimal(first_ip)
    last_ip = calculateIP(tmp, net_index, 1)
    last_valid_ip = calculateIPDecimal(last_ip)
    host_index = calculateIndex(given_subnet)
    first_subnet_end_ip = calculateIP(first_ip, host_index, 1)
    first_subnet_valid_end_ip = calculateIPDecimal(first_subnet_end_ip)
    differ_in_subnet = calculateDifferInSubnet(first_valid_ip, first_subnet_valid_end_ip)

    print("First valid IP: ", first_valid_ip)
    print("Last valid IP: ", last_valid_ip)
    print()
    calculateSubnetIPs(first_valid_ip, differ_in_subnet, first_subnet_valid_end_ip, last_valid_ip)
    input("")
    return 1


def calculateDifferInSubnet(ip1, ip2):
    ip1 = ip1.split(".")
    ip2 = ip2.split(".")
    tmp = [0, 0, 0, 0]
    i = 0
    while i < 4:
        if int(ip1[i]) != int(ip2[i]):
            tmp[i] = int(ip2[i]) - int(ip1[i])
            break
        i += 1
    return tmp


def calculateSubnetIPs(first_ip, differ, first_end_ip, last_ip):
    i = 0
    current_first_ip = first_ip.split(".")
    current_first_ip = [int(g) for g in current_first_ip]
    current_last_ip = first_end_ip.split(".")
    current_last_ip = [int(g) for g in current_last_ip]
    tmp_last_ip = last_ip.split(".")
    tmp_last_ip = [int(g) for g in tmp_last_ip]

    while i < 4:
        if int(differ[i]) != 0:
            break
        i += 1

    n = 1

    while 1:
        print("Subnet No: ", n)
        if n != 1:
            current_first_ip[i] = int(current_last_ip[i]) + 1
            current_first_ip, current_last_ip = sortIP(current_first_ip, current_last_ip, i)
        x = 3
        while x >= 0:
            if x != i:
                current_first_ip[x] = 0
                current_last_ip[x] = 255
                x = x - 1
                continue
            current_last_ip[i] = int(current_first_ip[i]) + int(differ[i])
            # current_last_ip[i-1] = int(current_first_ip[i-1])
            # current_last_ip = sortIP(current_last_ip,i)
            break

        current_first_valid_ip = ""
        current_last_valid_ip = ""
        y = 0
        while y < 4:
            if y != 0:
                current_first_valid_ip += "."
                current_last_valid_ip += "."
            current_first_valid_ip += str(current_first_ip[y])
            current_last_valid_ip += str(current_last_ip[y])
            y += 1

        print("First IP: ", current_first_valid_ip)
        print("Last IP: ", current_last_valid_ip)
        print("")
        a, b, c, d = current_last_ip
        a, b, c, d = int(a), int(b), int(c), int(d)
        e, f, g, h = tmp_last_ip
        e, f, g, h = int(e), int(f), int(g), int(h)
        if (a == e) & (b == f) & (c == g) & (d == h):
            break
        n += 1


def sortIP(tmpip, tmpip2, n):
    tmpip = tmpip.copy()
    tmpip2 = tmpip2.copy()
    i = n
    while i > 0:
        if int(tmpip[i]) >= 256:
            tmpip[i] -= 256
            x = int(tmpip[i - 1]) + 1
            y = int(tmpip2[i - 1]) + 1
            tmpip[i - 1] = x
            tmpip2[i - 1] = y
        i -= 1
    return tmpip, tmpip2


def calculateIP(ip, index, n):
    ip = ip.copy()
    i = index[0]
    j = index[1]
    while i < 4:
	#Project by Syed Umair Shah
        ip[i] = list(ip[i])
        while j < 8:
            ip[i][j] = str(n)
            j += 1
        ip[i] = "".join(ip[i])
        j = 0
        i += 1
    return ip


def calculateIPDecimal(ip):
    ip = ip.copy()
    i = 0
    tmp = ""
    while i < 4:
        if i != 0:
            tmp = tmp + "."
        tmp = tmp + str(binaryToDecimal(ip[i]))
        i += 1
    return tmp


def calculateIndex(n):
    n = int(n)
    tmp = []
    tmp.append(n // 8)
    tmp.append(n % 8)
    return tmp


def decToBinIP(ip):
    for x in ip:
        bin_ip.append(decimalToBinary(int(x)))


def decimalToBinary(n):
    return bin(n).replace("0b", "").zfill(8)


def binaryToDecimal(n):
    return int(n, 2)


def is_valid(ip):
    if len(ip) != 4:
        return 0

    for x in ip:
        try:
            y = int(x)
            if y < 0 or y > 255:
                return 0
        except:
            return 0

    return 1


def is_valid_slash_sub(subnet):
    if str(subnet[0]) == '/':
        try:
            x = int(subnet[1:])
            if x > 0 or x < 32:
                return 1
            return 0
        except:
            return 0
    else:
        return 0


def is_valid_given_sub(subnet):
    global given_subnet
    if not is_valid_slash_sub(subnet):
        return 0

    x = int(subnet[1:])
    given_subnet = x
    y = subnet_slash

    if x <= y:
        print("Required subnet can't be smaller than or equal to IP Subnet")
        return 0

    return 1


def is_valid_sub(subnet):
    global sub, bin_sub, net_index, subnet_slash

    if is_valid_slash_sub(subnet):
        try:
            subnet_slash = int(subnet[1:])
            x = subnet_slash
            net_index = calculateIndex(x)
            i = j = x = 0
            bin_sub = []
            while i < 4:
                bin_sub.append("")
                while j < 8:
                    if x < subnet_slash:
                        bin_sub[i] = bin_sub[i] + '1'
                    else:
                        bin_sub[i] = bin_sub[i] + '0'
                    x += 1
                    j += 1
                i += 1
                j = 0
        except:
            return 0

    else:

        sub = subnet.split(".")
        subnet = sub

        if not is_valid(subnet):
            return 0

        for x in subnet:
            bin_sub.append(decimalToBinary(int(x)))

        ld = int(bin_sub[0][0])

        if ld == 0:
            return 0

        i = j = 0
        while i < 4:
            j = 0
            while j < 8:
                ld = int(bin_sub[i][j])
                if ld:
                    j += 1
                    subnet_slash += 1
                else:
                    break
            if not ld:
                break
            i += 1
            j = 0

        net_index.append(i)
        net_index.append(j)
        while i < 4:
            while j < 8:
                ld = int(bin_sub[i][j])
                if not ld:
                    j += 1
                else:
                    break
            if ld:
                return 0
            i += 1
            j = 0

    return 1


def clear_variables():
    global ip, first_ip, first_valid_ip, first_subnet_end_ip, first_subnet_valid_end_ip, differ_in_subnet, last_ip, last_valid_ip, sub, subnet_slash, given_subnet, bin_ip, bin_sub, net_index, host_index, subnet_groups
    ip = []
    first_ip = []
    first_valid_ip = ""
    first_subnet_end_ip = []
    first_subnet_valid_end_ip = ""
    differ_in_subnet = []
    last_ip = []
    last_valid_ip = ""
    sub = []
    subnet_slash = 0
    given_subnet = 0
    bin_ip = []
    bin_sub = []
    net_index = []
    host_index = []
    subnet_groups = []


while not finished:
    finished = start()
