import sys

start = int(sys.argv[1])
end = int(sys.argv[2])
arr = [str(i) for i in range(start, end)]
print(','.join(arr))