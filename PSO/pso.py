import math
import random

from typing import List, Any

from animation import show_animation

class Partical:
    def __init__(self, dimention_of_variable: int, variable_range: tuple[float, float]):
        self._pos = [ 0.0 for _ in range(dimention_of_variable) ]
        self._v   = [ 0.0 for _ in range(dimention_of_variable) ]

        self._variable_range = variable_range
        self._dimention_of_variable = dimention_of_variable
        
        self._v_max = 0.01 * (variable_range[1] - variable_range[0])
        self._v_min = 0.01 * (variable_range[0] - variable_range[1])

        self.random_pos()
        
        self._local_best_pos = self._pos.copy()
        self._local_best_score = self.fitness_score()
    
    def update_local_best(self):
        if self.fitness_score() < self._local_best_score:
            self._local_best_pos = self._pos
            self._local_best_score = self.fitness_score()
        
    def get_pos(self):
        return self._pos

    def get_v(self):
        return self._v
    
    def random_pos(self):
        for d in range(self._dimention_of_variable):
            val = random.random() * abs(self._variable_range[0] - self._variable_range[1]) + self._variable_range[0]
            while abs(val) < self._variable_range[1] / 1.5: # 避免生成在原點附近
                val = random.random() * abs(self._variable_range[0] - self._variable_range[1]) + self._variable_range[0]
            self._pos[d] = val

    def update_pos(self, global_best_pos, c1=1.0, c2=1.0, t=None, t_max=None):
        for d, _ in enumerate(self._v):
            self._pos[d] += self._v[d]
            self._pos[d] = min(self._pos[d], self._variable_range[1])
            self._pos[d] = max(self._pos[d], self._variable_range[0])
            
            if t is not None and t_max is not None:
                self._w = 1.5 - (1.5 - 0.1) * (t / t_max)
            
            r1 = random.random()
            r2 = random.random()
            
            self._v[d] = self._w * self._v[d] + c1 * r1 * (self._local_best_pos[d] - self._pos[d]) + c2 * r2 * (global_best_pos[d] - self._pos[d])
            
        self.normalization_velocity()
        self.update_local_best()
    
    def normalization_velocity(self):
        sum_num = 0
        for v in self._v:
            sum_num += v ** 2
        sum_v = math.sqrt(sum_num)
        if sum_v > self._v_max:
            for i, _ in enumerate(self._v):
                self._v[i] *= (self._v_max / sum_v)

    def fitness_score(self):
        # 假設評分函數 f(x) = x ^ 2 + y ^ 2 + z ^ 2 ...
        pos = self.get_pos()
        return sum([n ** 2 for n in pos])

class PSO_Algorithm:
    def __init__(self, dimention_of_variable: int, variable_range: tuple[float, float]):
        self._global_best_pos = [0.0, 0.0]
        self._global_best_score = math.inf
        self._recorded_frame: dict[str, dict] = {}
        self.particals : List[Partical] = []
        
        self._dimention_of_variable = dimention_of_variable
        self._variable_range = variable_range
        
        self._t = 0
    
    def search(self, t_max = 200):
        for partical in self.particals:
            partical.update_pos(self._global_best_pos, t=self._t, t_max=t_max)
            self.update_global_best(partical)
        
        self.record_frame(self._t)
        self._t += 1
    
    def update_global_best(self, partical: Partical):
        if partical.fitness_score() < self._global_best_score:
            self._global_best_pos = partical.get_pos().copy()
            self._global_best_score = partical.fitness_score()
    
    def create_particals(self, num):
        for _ in range(num):
            partical = Partical(self._dimention_of_variable, self._variable_range)
            self.particals.append(partical)
            self.update_global_best(partical)

    def get_best_parameter(self):
        return self._global_best_score, self._global_best_pos
    
    def record_frame(self, t: int):
        data: dict[str, Any] = {}
        for i, partical in enumerate(self.particals):
            data[f'particle_{i}'] = { 'pos': partical.get_pos().copy(), 'v': partical.get_v().copy() }
        data['global_best'] = self._global_best_pos.copy()
        self._recorded_frame[f't_{t}'] = data
    
    def get_recorded_frames(self):
        return self._recorded_frame

def PSO_test_run():
    """
    Please make your pso algorithm can be excute by following scripts.
    Feel free to add arguments when initializing algorithm if it is needed.
        For example: PSO_Algorithm(dimention_of_variable, variable_range)
    """
    pso = PSO_Algorithm(2, (-100.0, 100.0))
    pso.create_particals(10)
    
    total_epoch = 200
    for _ in range(total_epoch):
        pso.search(t_max=total_epoch)
        
    print(pso.get_best_parameter())
    
    show_animation(pso.get_recorded_frames())
    
if __name__ == '__main__':
    PSO_test_run()