from Detection import Detection

# detect = Detection([1,3,5]) # ordinal
# print(detect.type)
#
# detect = Detection([1,2,3,4,5]) # ordinal
# print(detect.type)
#
#
#
#
# # why is this not categorical
# detect = Detection([1,1,3,3,3,3,3,5])  # ratiointerval
# print(detect.type)
#
# detect = Detection([1,1,1,1,3,3,3,3,3,5,5,5,5]) # categorical
# print(detect.type)
#
# detect = Detection([2,4,6,8,10]) # sequential
# print(detect.type)
#
# detect = Detection([2,5,6,8,10]) # sequential
# print(detect.type)
#
# detect = Detection([0,2,4,6,9,12,15]) # sequential
# print(detect.type)
#
#
# detect = Detection([12312,12327,12339,12347,12358]) # hierarchical
# print(detect.type)
#
# detect = Detection([28,456,2,18,12358]) # ratiointerval
# print(detect.type)
#
# detect = Detection([28.5,456,2,18,12358]) # ratiointerval
# print(detect.type)
#
# detect = Detection([28,456,2,18,-12358]) # ratiointerval
# print(detect.type)
#
#
# detect = Detection([1,1,1,1,1]) # ratiointerval
# print(detect.type)

detect = Detection([182,126,115,101,30,3,2,2,1,0,0,0,0,0,0,20,582])
print(detect.type)
