from scipy.special import comb


# 针对sire形式计算CC程序
class Renode:  # 定义cc结点类
    def __init__(self, regl=None, ccnum=0):
        self.regl = regl
        self.ccnum = ccnum

    def reg(self, regl):
        self.reg = regl

    def cnum(self, ccnum):
        self.ccnum = ccnum

def takecc(node):
    return  node.ccnum
def split_regex(regex):
    regex = regex.replace("+", "").replace("?", "").replace("*", "")
    return regex.split("&")


def cnt_cc(elems):
    nums = [elem.count(",") + 1 for elem in elems]
    cc, sum_num = 1, nums[0]
    for i in range(0, len(nums)):
        if i + 1 < len(nums):
            sum_num += nums[i + 1]
            cc *= comb(sum_num, nums[i + 1])

    return cc


def Rankcc(Relist):
    cclist = []
    for i in Relist:
        regex = i

        elems = split_regex(regex)
        cc = cnt_cc(elems)
        node = Renode(i,cc)
        cclist.append(node)


    cclist.sort(key=takecc)
    return  cclist
# from scipy.special import comb
# # 针对sire形式计算CC程序
# def split_regex(regex):
#     regex = regex.replace("+", "").replace("?", "").replace("*", "")
#     return regex.split("&")
#
# def cnt_cc(elems):
#     nums = [elem.count(",")+1 for elem in elems]
#     cc, sum_num = 1, nums[0]
#     for i in range(0, len(nums)):
#         if i+1 < len(nums):
#             sum_num += nums[i+1]
#             cc*= comb(sum_num, nums[i+1])
#
#     return cc
#
#
#
# if __name__ == '__main__':
#     regex = "booktitle?,month?,cdrom?,note*&year?&journal?&title+,crossref?,number?,publisher?,cite*&url?&volume?&author*,pages?&editor*,ee*"
#     print(regex)
#     elems = split_regex(regex)
#     print(elems)
#     cc = cnt_cc(elems)
#     print(cc)
