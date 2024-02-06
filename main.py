class Solution:
    def soortbeta(self, nums: list[int]) -> list[int]:
        n = len(nums)
        while True:
            cnt = 0
            for i in range(n - 1 - cnt):
                if nums[i] > nums[i + 1]:
                    nums[i], nums[i + 1] = nums[i + 1], nums[i]
                    cnt += 1
            if not cnt:
                break
        return nums


k = [int(i) for i in input().split()]
sol = Solution()
print(*sol.soortbeta(k))
