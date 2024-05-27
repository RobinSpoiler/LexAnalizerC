def twoSum(nums, target):
    numMap = {}
    n = len(nums)
    for i in range(n):
        numMap[nums[i]] = i
    for i in range(n):
        complement = target - nums[i]
        if complement in numMap and numMap[complement] != i:
            return [i, numMap[complement]]
    return [] 