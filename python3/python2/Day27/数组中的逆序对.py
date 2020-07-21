""" 欢迎关注 "码农架构" 微信公众号，热爱开源，拥抱开源。一个IT民工的技术之路经验分享。
    - 问题咨询 / 建议
    1.关注微信公众号 "码农架构" 后私信
    2.可发送邮件: li.shangzhi@aliyun.com
"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/27 14:55
# @Author  : iByte

"""
在数组中的两个数字如果前面一个数字大于后面的数字，则这两个数字组成一个逆序对。

输入一个数组，求出这个数组中的逆序对的总数。

样例
输入：[1,2,3,4,5,6,0]

输出：6
"""

def inversePairs(self, nums):
    """
    :type nums: List[int]
    :rtype: int
    """

    l = len(nums)
    if l < 2:
        return 0
    temp = [0 for _ in range(l)]
    return self.count_inversion_pairs(nums, 0, l - 1, temp)


def count_inversion_pairs(self, nums, l, r, temp):
    """
    在数组 nums 的区间 [l,r] 统计逆序对
    :param nums:
    :param l: 待统计数组的左边界，可以取到
    :param r: 待统计数组的右边界，可以取到
    :param temp:
    :return:
    """
    # 极端情况下，就是只有 1 个元素的时候
    if l == r:
        return 0
    mid = l + (r - l) // 2
    left_pairs = self.count_inversion_pairs(nums, l, mid, temp)
    right_pairs = self.count_inversion_pairs(nums, mid + 1, r, temp)

    merge_pairs = 0
    # 代码走到这里的时候，
    # [l, mid] 已经完成了排序并且计算好逆序对
    # [mid + 1, r] 已经完成了排序并且计算好逆序对
    # 如果 nums[mid] <= nums[mid + 1]，此时就不存在逆序对
    # 当 nums[mid] > nums[mid + 1] 的时候，就要继续计算逆序对
    if nums[mid] > nums[mid + 1]:
        # 在归并的过程中计算逆序对
        merge_pairs = self.merge_and_count(nums, l, mid, r, temp)
    # 走到这里有 nums[mid] <= nums[mid + 1] 成立，已经是顺序结构
    return left_pairs + right_pairs + merge_pairs


def merge_and_count(self, nums, l, mid, r, temp):
    """
    前：[2,3,5,8]，后：[4,6,7,12]
    我们只需要在后面数组元素出列的时候，数一数前面这个数组还剩下多少个数字，
    因为"前"数组和"后"数组都有序，
    因此，"前"数组剩下的元素个数 mid - i + 1 就是与"后"数组元素出列的这个元素构成的逆序对个数

    """
    for i in range(l, r + 1):
        temp[i] = nums[i]
    i = l
    j = mid + 1
    res = 0
    for k in range(l, r + 1):
        if i > mid:
            nums[k] = temp[j]
            j += 1
        elif j > r:
            nums[k] = temp[i]
            i += 1
        elif temp[i] <= temp[j]:
            # 不统计逆序对，只做排序
            nums[k] = temp[i]
            i += 1
        else:
            assert temp[i] > temp[j]
            nums[k] = temp[j]
            j += 1
            # 快就快在这里，一次可以数出一个区间的个数的逆序对
            # 例：[7,8,9][4,6,9]，4 与 7 以及 7 前面所有的数都构成逆序对
            res += (mid - i + 1)
    return res

if __name__ == '__main__':
