from math import sqrt as sqrt
import heapq
import numpy as np

class Telea():
    def __init__(self):

        self.KNOWN = 0
        self.BAND = 1
        self.UNKNOWN = 2

        self.INF = 1e6
        self.EPS = 1e-6

    def _solve_eikonal(self, y1, x1, y2, x2, height, width, dists, flags):
        if y1 < 0 or y1 >= height or x1 < 0 or x1 >= width:
            return self.INF

        if y2 < 0 or y2 >= height or x2 < 0 or x2 >= width:
            return self.INF

        flag1 = flags[y1, x1]
        flag2 = flags[y2, x2]

        if flag1 == self.KNOWN and flag2 == self.KNOWN:
            dist1 = dists[y1, x1]
            dist2 = dists[y2, x2]
            d = 2.0 - (dist1 - dist2) ** 2
            if d > 0.0:
                r = sqrt(d)
                s = (dist1 + dist2 - r) / 2.0
                if s >= dist1 and s >= dist2:
                    return s
                s += r
                if s >= dist1 and s >= dist2:
                    return s

                return self.INF

        if flag1 == self.KNOWN:
            dist1 = dists[y1, x1]
            return 1.0 + dist1

        if flag2 == self.KNOWN:
            dist2 = dists[y2, x2]
            return 1.0 + dist2

        return self.INF

    def _pixel_gradient(self, y, x, height, width, vals, flags):
        val = vals[y, x]

        prev_y = y - 1
        next_y = y + 1
        if prev_y < 0 or next_y >= height:
            grad_y = self.INF
        else:
            flag_prev_y = flags[prev_y, x]
            flag_next_y = flags[next_y, x]

            if flag_prev_y != self.UNKNOWN and flag_next_y != self.UNKNOWN:
                grad_y = (vals[next_y, x] - vals[prev_y, x]) / 2.0
            elif flag_prev_y != self.UNKNOWN:
                grad_y = val - vals[prev_y, x]
            elif flag_next_y != self.UNKNOWN:
                grad_y = vals[next_y, x] - val
            else:
                grad_y = 0.0

        prev_x = x - 1
        next_x = x + 1
        if prev_x < 0 or next_x >= width:
            grad_x = self.INF
        else:
            flag_prev_x = flags[y, prev_x]
            flag_next_x = flags[y, next_x]

            if flag_prev_x != self.UNKNOWN and flag_next_x != self.UNKNOWN:
                grad_x = (vals[y, next_x] - vals[y, prev_x]) / 2.0
            elif flag_prev_x != self.UNKNOWN:
                grad_x = val - vals[y, prev_x]
            elif flag_next_x != self.UNKNOWN:
                grad_x = vals[y, next_x] - val
            else:
                grad_x = 0.0

        return grad_y, grad_x

    def _compute_outside_dists(self, height, width, dists, flags, band, radius):
        band = band.copy()
        orig_flags = flags
        flags = orig_flags.copy()
        # swap INSIDE / OUTSIDE
        flags[orig_flags == self.KNOWN] = self.UNKNOWN
        flags[orig_flags == self.UNKNOWN] = self.KNOWN

        last_dist = 0.0
        double_radius = radius * 2
        while band:
            if last_dist >= double_radius:
                break

            _, y, x = heapq.heappop(band)
            flags[y, x] = self.KNOWN

            neighbors = [(y - 1, x), (y, x - 1), (y + 1, x), (y, x + 1)]
            for nb_y, nb_x in neighbors:
                if nb_y < 0 or nb_y >= height or nb_x < 0 or nb_x >= width:
                    continue

                if flags[nb_y, nb_x] != self.UNKNOWN:
                    continue

                last_dist = min([
                    self._solve_eikonal(nb_y - 1, nb_x, nb_y, nb_x - 1, height, width, dists, flags),
                    self._solve_eikonal(nb_y + 1, nb_x, nb_y, nb_x + 1, height, width, dists, flags),
                    self._solve_eikonal(nb_y - 1, nb_x, nb_y, nb_x + 1, height, width, dists, flags),
                    self._solve_eikonal(nb_y + 1, nb_x, nb_y, nb_x - 1, height, width, dists, flags)
                ])
                dists[nb_y, nb_x] = last_dist

                flags[nb_y, nb_x] = self.BAND
                heapq.heappush(band, (last_dist, nb_y, nb_x))

        dists *= -1.0

    def _init(self, height, width, mask, radius):
        dists = np.full((height, width), self.INF, dtype=float)
        flags = mask.astype(int) * self.UNKNOWN
        band = []

        mask_y, mask_x = mask.nonzero()
        for y, x in zip(mask_y, mask_x):
            neighbors = [(y - 1, x), (y, x - 1), (y + 1, x), (y, x + 1)]
            for nb_y, nb_x in neighbors:
                if nb_y < 0 or nb_y >= height or nb_x < 0 or nb_x >= width:
                    continue

                if flags[nb_y, nb_x] == self.BAND:
                    continue

                if mask[nb_y, nb_x] == 0:
                    flags[nb_y, nb_x] = self.BAND
                    dists[nb_y, nb_x] = 0.0
                    heapq.heappush(band, (0.0, nb_y, nb_x))

        self._compute_outside_dists(height, width, dists, flags, band, radius)

        return dists, flags, band

    def _inpaint_pixel(self, y, x, img, height, width, dists, flags, radius):
        dist = dists[y, x]
        dist_grad_y, dist_grad_x = self._pixel_gradient(y, x, height, width, dists, flags)
        pixel_sum = np.zeros((3), dtype=float)
        weight_sum = 0.0

        for nb_y in range(y - radius, y + radius + 1):
            if nb_y < 0 or nb_y >= height:
                continue

            for nb_x in range(x - radius, x + radius + 1):
                if nb_x < 0 or nb_x >= width:
                    continue

                if flags[nb_y, nb_x] == self.UNKNOWN:
                    continue

                dir_y = y - nb_y
                dir_x = x - nb_x
                dir_length_square = dir_y ** 2 + dir_x ** 2
                dir_length = sqrt(dir_length_square)
                if dir_length > radius:
                    continue

                dir_factor = abs(dir_y * dist_grad_y + dir_x * dist_grad_x)
                if dir_factor == 0.0:
                    dir_factor = self.EPS

                nb_dist = dists[nb_y, nb_x]
                level_factor = 1.0 / (1.0 + abs(nb_dist - dist))

                dist_factor = 1.0 / (dir_length * dir_length_square)

                weight = abs(dir_factor * dist_factor * level_factor)

                pixel_sum[0] += weight * img[nb_y, nb_x, 0]
                pixel_sum[1] += weight * img[nb_y, nb_x, 1]
                pixel_sum[2] += weight * img[nb_y, nb_x, 2]

                weight_sum += weight

        return pixel_sum / weight_sum

    def inpaint(self, img, mask, radius=5):
        if img.shape[0:2] != mask.shape[0:2]:
            raise ValueError("Image and mask dimensions do not match")

        height, width = img.shape[0:2]
        dists, flags, band = self._init(height, width, mask, radius)

        while band:
            _, y, x = heapq.heappop(band)
            flags[y, x] = self.KNOWN

            neighbors = [(y - 1, x), (y, x - 1), (y + 1, x), (y, x + 1)]
            for nb_y, nb_x in neighbors:
                if nb_y < 0 or nb_y >= height or nb_x < 0 or nb_x >= width:
                    continue

                if flags[nb_y, nb_x] != self.UNKNOWN:
                    continue

                nb_dist = min([
                    self._solve_eikonal(nb_y - 1, nb_x, nb_y, nb_x - 1, height, width, dists, flags),
                    self._solve_eikonal(nb_y + 1, nb_x, nb_y, nb_x + 1, height, width, dists, flags),
                    self._solve_eikonal(nb_y - 1, nb_x, nb_y, nb_x + 1, height, width, dists, flags),
                    self._solve_eikonal(nb_y + 1, nb_x, nb_y, nb_x - 1, height, width, dists, flags)
                ])
                dists[nb_y, nb_x] = nb_dist

                pixel_vals = self._inpaint_pixel(nb_y, nb_x, img, height, width, dists, flags, radius)

                img[nb_y, nb_x, 0] = pixel_vals[0]
                img[nb_y, nb_x, 1] = pixel_vals[1]
                img[nb_y, nb_x, 2] = pixel_vals[2]

                flags[nb_y, nb_x] = self.BAND

                heapq.heappush(band, (nb_dist, nb_y, nb_x))
