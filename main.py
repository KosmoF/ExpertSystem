import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class Power(Enum):
    HIGH = "высокая"
    MEDIUM = "средняя"
    LOW = "низкая"

class MaxSpeed(Enum):
    HIGH = "высокая"
    MEDIUM = "средняя"
    LOW = "низкая"

class Clearance(Enum):
    BIG = "большой"
    MEDIUM = "средний"
    SMALL = "маленький"

class TrunkVolume(Enum):
    BIG = "большой"
    MEDIUM = "средний"
    SMALL = "маленький"

class FuelConsumption(Enum):
    BIG = "большой"
    MEDIUM = "средний"
    SMALL = "маленький"

class Dynamics(Enum):
    HIGH = "высокая"
    MEDIUM = "средняя"
    LOW = "низкая"

class Budget(Enum):
    VERY_HIGH = "очень высокий"
    HIGH = "высокий"
    MEDIUM = "средний"
    LOW = "низкий"
    VERY_LOW = "очень низкий"

# Data structure for car specifications
@dataclass
class CarSpecs:
    name: str
    power: Power
    max_speed: MaxSpeed
    clearance: Clearance
    trunk_volume: TrunkVolume
    fuel_consumption: FuelConsumption
    dynamics: Dynamics
    price: int

# Fuzzy membership functions
def triangular(x: float, a: float, b: float, c: float) -> float:
    if x <= a or x >= c:
        return 0.0
    elif a <= x <= b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)

def trapezoidal(x: float, a: float, b: float, c: float, d: float) -> float:
    if x <= a or x >= d:
        return 0.0
    elif b <= x <= c:
        return 1.0
    elif a <= x <= b:
        return (x - a) / (b - a)
    else:
        return (d - x) / (d - c)

def gaussian(x: float, c: float, sigma: float) -> float:
    return np.exp(-((x - c) ** 2) / (2 * sigma ** 2))

def generalized_gaussian(x: float, c: float, sigma: float, p: float) -> float:
    return np.exp(-((x - c) ** p) / (2 * sigma ** p))

# Defuzzification methods
def center_of_gravity(x: np.ndarray, y: np.ndarray) -> float:
    return np.sum(x * y) / np.sum(y)

def mean_of_maximum(x: np.ndarray, y: np.ndarray) -> float:
    max_y = np.max(y)
    max_indices = np.where(y == max_y)[0]
    return np.mean(x[max_indices])

def maximum_membership(x: np.ndarray, y: np.ndarray) -> float:
    return x[np.argmax(y)]

# Car database
cars = [
    CarSpecs("Lada Granta", Power.LOW, MaxSpeed.LOW, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.SMALL, Dynamics.LOW, 800000),
    CarSpecs("Lada Vesta", Power.LOW, MaxSpeed.MEDIUM, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.MEDIUM, Dynamics.LOW, 1200000),
    CarSpecs("Kia Rio", Power.MEDIUM, MaxSpeed.MEDIUM, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.MEDIUM, Dynamics.MEDIUM, 1500000),
    CarSpecs("Hyundai Solaris", Power.MEDIUM, MaxSpeed.MEDIUM, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.MEDIUM, Dynamics.MEDIUM, 1400000),
    CarSpecs("Volkswagen Polo", Power.MEDIUM, MaxSpeed.MEDIUM, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.MEDIUM, Dynamics.MEDIUM, 1600000),
    CarSpecs("Skoda Rapid", Power.MEDIUM, MaxSpeed.MEDIUM, Clearance.MEDIUM, TrunkVolume.BIG, FuelConsumption.MEDIUM, Dynamics.MEDIUM, 1700000),
    CarSpecs("Toyota Camry", Power.HIGH, MaxSpeed.HIGH, Clearance.MEDIUM, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.HIGH, 2500000),
    CarSpecs("Nissan X-Trail", Power.HIGH, MaxSpeed.MEDIUM, Clearance.BIG, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.MEDIUM, 2800000),
    CarSpecs("Mitsubishi Outlander", Power.HIGH, MaxSpeed.MEDIUM, Clearance.BIG, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.MEDIUM, 2600000),
    CarSpecs("Honda CR-V", Power.HIGH, MaxSpeed.MEDIUM, Clearance.BIG, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.MEDIUM, 3000000),
    CarSpecs("Mazda CX-5", Power.HIGH, MaxSpeed.HIGH, Clearance.BIG, TrunkVolume.BIG, FuelConsumption.MEDIUM, Dynamics.HIGH, 2900000),
    CarSpecs("Subaru Forester", Power.HIGH, MaxSpeed.MEDIUM, Clearance.BIG, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.MEDIUM, 2700000),
    CarSpecs("Volkswagen Tiguan", Power.HIGH, MaxSpeed.HIGH, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.MEDIUM, Dynamics.HIGH, 3200000),
    CarSpecs("Skoda Kodiaq", Power.HIGH, MaxSpeed.HIGH, Clearance.BIG, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.HIGH, 3100000),
    CarSpecs("Audi Q5", Power.HIGH, MaxSpeed.HIGH, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.BIG, Dynamics.HIGH, 4500000),
    CarSpecs("BMW X3", Power.HIGH, MaxSpeed.HIGH, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.BIG, Dynamics.HIGH, 4800000),
    CarSpecs("Mercedes-Benz GLC", Power.HIGH, MaxSpeed.HIGH, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.BIG, Dynamics.HIGH, 5000000),
    CarSpecs("Lexus RX", Power.HIGH, MaxSpeed.HIGH, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.BIG, Dynamics.HIGH, 5500000),
    CarSpecs("Porsche Cayenne", Power.HIGH, MaxSpeed.HIGH, Clearance.MEDIUM, TrunkVolume.MEDIUM, FuelConsumption.BIG, Dynamics.HIGH, 8000000),
    CarSpecs("Range Rover Sport", Power.HIGH, MaxSpeed.HIGH, Clearance.BIG, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.HIGH, 9000000),
    CarSpecs("Lada Niva", Power.LOW, MaxSpeed.LOW, Clearance.BIG, TrunkVolume.SMALL, FuelConsumption.MEDIUM, Dynamics.LOW, 1000000),
    CarSpecs("UAZ Patriot", Power.LOW, MaxSpeed.LOW, Clearance.BIG, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.LOW, 1500000),
    CarSpecs("Renault Duster", Power.MEDIUM, MaxSpeed.MEDIUM, Clearance.BIG, TrunkVolume.MEDIUM, FuelConsumption.MEDIUM, Dynamics.MEDIUM, 1800000),
    CarSpecs("Suzuki Vitara", Power.MEDIUM, MaxSpeed.MEDIUM, Clearance.BIG, TrunkVolume.MEDIUM, FuelConsumption.MEDIUM, Dynamics.MEDIUM, 1900000),
    CarSpecs("Toyota RAV4", Power.HIGH, MaxSpeed.HIGH, Clearance.BIG, TrunkVolume.MEDIUM, FuelConsumption.MEDIUM, Dynamics.HIGH, 3500000),
    CarSpecs("Kia Sportage", Power.MEDIUM, MaxSpeed.MEDIUM, Clearance.BIG, TrunkVolume.MEDIUM, FuelConsumption.MEDIUM, Dynamics.MEDIUM, 2200000),
    CarSpecs("Hyundai Tucson", Power.MEDIUM, MaxSpeed.MEDIUM, Clearance.BIG, TrunkVolume.MEDIUM, FuelConsumption.MEDIUM, Dynamics.MEDIUM, 2300000),
    CarSpecs("Ford Explorer", Power.HIGH, MaxSpeed.HIGH, Clearance.BIG, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.HIGH, 4000000),
    CarSpecs("Jeep Grand Cherokee", Power.HIGH, MaxSpeed.HIGH, Clearance.BIG, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.HIGH, 4200000),
    CarSpecs("Volvo XC90", Power.HIGH, MaxSpeed.HIGH, Clearance.MEDIUM, TrunkVolume.BIG, FuelConsumption.BIG, Dynamics.HIGH, 6000000)
]

# Fuzzy rules database (30 rules)
fuzzy_rules = [
    # Rule 1: Если все параметры низкие -> очень низкий бюджет
    {
        "if": {
            "мощность": "низкая",
            "макс. скорость": "низкая",
            "клиренс": "маленький",
            "объем багажника": "маленький",
            "расход топлива": "маленький",
            "динамика": "низкая"
        },
        "then": {"бюджет": Budget.VERY_LOW}
    },
    # Rule 2: Если большинство параметров низкие, но есть средние -> низкий бюджет
    {
        "if": {
            "мощность": "низкая",
            "макс. скорость": "средняя",
            "клиренс": "маленький",
            "объем багажника": "маленький",
            "расход топлива": "маленький",
            "динамика": "низкая"
        },
        "then": {"бюджет": Budget.LOW}
    },
    # Rule 3: Если половина параметров низкие, половина средние -> низкий бюджет
    {
        "if": {
            "мощность": "низкая",
            "макс. скорость": "средняя",
            "клиренс": "маленький",
            "объем багажника": "средний",
            "расход топлива": "маленький",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.LOW}
    },
    # Rule 4: Если большинство параметров средние, есть низкие -> низкий бюджет
    {
        "if": {
            "мощность": "средняя",
            "макс. скорость": "средняя",
            "клиренс": "маленький",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.LOW}
    },
    # Rule 5: Если все параметры средние -> средний бюджет
    {
        "if": {
            "мощность": "средняя",
            "макс. скорость": "средняя",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 6: Если большинство параметров средние, есть высокие -> средний бюджет
    {
        "if": {
            "мощность": "средняя",
            "макс. скорость": "высокая",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 7: Если половина параметров средние, половина высокие -> средний бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "высокая",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 8: Если большинство параметров высокие, есть средние -> высокий бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "высокая",
            "клиренс": "средний",
            "объем багажника": "большой",
            "расход топлива": "большой",
            "динамика": "высокая"
        },
        "then": {"бюджет": Budget.HIGH}
    },
    # Rule 9: Если все параметры высокие -> очень высокий бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "высокая",
            "клиренс": "большой",
            "объем багажника": "большой",
            "расход топлива": "большой",
            "динамика": "высокая"
        },
        "then": {"бюджет": Budget.VERY_HIGH}
    },
    # Rule 10: Если мощность высокая, остальные средние -> средний бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "средняя",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 11: Если динамика высокая, остальные средние -> средний бюджет
    {
        "if": {
            "мощность": "средняя",
            "макс. скорость": "средняя",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "высокая"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 12: Если клиренс большой, остальные средние -> средний бюджет
    {
        "if": {
            "мощность": "средняя",
            "макс. скорость": "средняя",
            "клиренс": "большой",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 13: Если объем багажника большой, остальные средние -> средний бюджет
    {
        "if": {
            "мощность": "средняя",
            "макс. скорость": "средняя",
            "клиренс": "средний",
            "объем багажника": "большой",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 14: Если расход топлива большой, остальные средние -> средний бюджет
    {
        "if": {
            "мощность": "средняя",
            "макс. скорость": "средняя",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "большой",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 15: Если мощность и динамика высокие, остальные средние -> высокий бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "средняя",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "высокая"
        },
        "then": {"бюджет": Budget.HIGH}
    },
    # Rule 16: Если мощность и скорость высокие, остальные средние -> высокий бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "высокая",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.HIGH}
    },
    # Rule 17: Если мощность и клиренс высокие, остальные средние -> высокий бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "средняя",
            "клиренс": "большой",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.HIGH}
    },
    # Rule 18: Если мощность и багажник высокие, остальные средние -> высокий бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "средняя",
            "клиренс": "средний",
            "объем багажника": "большой",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.HIGH}
    },
    # Rule 19: Если мощность и расход высокие, остальные средние -> высокий бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "средняя",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "большой",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.HIGH}
    },
    # Rule 20: Если три параметра высокие, три средние -> высокий бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "высокая",
            "клиренс": "большой",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.HIGH}
    },
    # Rule 21: Если четыре параметра высокие, два средние -> очень высокий бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "высокая",
            "клиренс": "большой",
            "объем багажника": "большой",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.VERY_HIGH}
    },
    # Rule 22: Если пять параметров высокие, один средний -> очень высокий бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "высокая",
            "клиренс": "большой",
            "объем багажника": "большой",
            "расход топлива": "большой",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.VERY_HIGH}
    },
    # Rule 23: Если два параметра низкие, четыре средние -> низкий бюджет
    {
        "if": {
            "мощность": "низкая",
            "макс. скорость": "низкая",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.LOW}
    },
    # Rule 24: Если три параметра низкие, три средние -> низкий бюджет
    {
        "if": {
            "мощность": "низкая",
            "макс. скорость": "низкая",
            "клиренс": "маленький",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.LOW}
    },
    # Rule 25: Если четыре параметра низкие, два средние -> очень низкий бюджет
    {
        "if": {
            "мощность": "низкая",
            "макс. скорость": "низкая",
            "клиренс": "маленький",
            "объем багажника": "маленький",
            "расход топлива": "средний",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.VERY_LOW}
    },
    # Rule 26: Если пять параметров низкие, один средний -> очень низкий бюджет
    {
        "if": {
            "мощность": "низкая",
            "макс. скорость": "низкая",
            "клиренс": "маленький",
            "объем багажника": "маленький",
            "расход топлива": "маленький",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.VERY_LOW}
    },
    # Rule 27: Если все параметры средние, кроме одного высокого -> средний бюджет
    {
        "if": {
            "мощность": "средняя",
            "макс. скорость": "средняя",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "средний",
            "динамика": "высокая"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 28: Если все параметры средние, кроме одного низкого -> средний бюджет
    {
        "if": {
            "мощность": "средняя",
            "макс. скорость": "средняя",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "маленький",
            "динамика": "средняя"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 29: Если два параметра высокие, два средние, два низкие -> средний бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "высокая",
            "клиренс": "средний",
            "объем багажника": "средний",
            "расход топлива": "маленький",
            "динамика": "низкая"
        },
        "then": {"бюджет": Budget.MEDIUM}
    },
    # Rule 30: Если три параметра высокие, три низкие -> средний бюджет
    {
        "if": {
            "мощность": "высокая",
            "макс. скорость": "высокая",
            "клиренс": "большой",
            "объем багажника": "маленький",
            "расход топлива": "маленький",
            "динамика": "низкая"
        },
        "then": {"бюджет": Budget.MEDIUM}
    }
]

# Fuzzy membership function parameters
FUZZY_PARAMS = {
    "мощность": {
        "низкая": {"type": "triangular", "params": [1, 3, 5]},
        "средняя": {"type": "triangular", "params": [3, 5, 7]},
        "высокая": {"type": "triangular", "params": [5, 7, 10]}
    },
    "макс. скорость": {
        "низкая": {"type": "triangular", "params": [1, 3, 5]},
        "средняя": {"type": "triangular", "params": [3, 5, 7]},
        "высокая": {"type": "triangular", "params": [5, 7, 10]}
    },
    "клиренс": {
        "маленький": {"type": "triangular", "params": [1, 3, 5]},
        "средний": {"type": "triangular", "params": [3, 5, 7]},
        "большой": {"type": "triangular", "params": [5, 7, 10]}
    },
    "объем багажника": {
        "маленький": {"type": "triangular", "params": [1, 3, 5]},
        "средний": {"type": "triangular", "params": [3, 5, 7]},
        "большой": {"type": "triangular", "params": [5, 7, 10]}
    },
    "расход топлива": {
        "маленький": {"type": "triangular", "params": [1, 3, 5]},
        "средний": {"type": "triangular", "params": [3, 5, 7]},
        "большой": {"type": "triangular", "params": [5, 7, 10]}
    },
    "динамика": {
        "низкая": {"type": "triangular", "params": [1, 3, 5]},
        "средняя": {"type": "triangular", "params": [3, 5, 7]},
        "высокая": {"type": "triangular", "params": [5, 7, 10]}
    }
}

# Budget membership function parameters
BUDGET_PARAMS = {
    "очень низкий": {"type": "triangular", "params": [500000, 1000000, 2000000]},
    "низкий": {"type": "triangular", "params": [1000000, 2000000, 3000000]},
    "средний": {"type": "triangular", "params": [2000000, 3500000, 5000000]},
    "высокий": {"type": "triangular", "params": [3000000, 5000000, 7000000]},
    "очень высокий": {"type": "triangular", "params": [5000000, 7000000, 9000000]}
}

class CarExpertSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Экспертная система подбора автомобиля")
        self.root.geometry("480x640")

        self.create_widgets()

    def create_widgets(self):
        # Notebook для разных режимов работы
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка для четкой ЭС (прямая цепочка)
        self.crisp_forward_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.crisp_forward_frame, text="Четкая ЭС (прямая)")

        # Вкладка для четкой ЭС (обратная цепочка)
        self.crisp_backward_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.crisp_backward_frame, text="Четкая ЭС (обратная)")

        # Вкладка для нечеткой ЭС
        self.fuzzy_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.fuzzy_frame, text="Нечеткая ЭС")

        # Создаем содержимое каждой вкладки
        self.create_crisp_forward_widgets()
        self.create_crisp_backward_widgets()
        self.create_fuzzy_widgets()

        # Поле для вывода результатов
        self.result_text = scrolledtext.ScrolledText(self.root, width=100, height=20)
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def create_crisp_forward_widgets(self):
        # Параметры автомобиля
        ttk.Label(self.crisp_forward_frame, text="Мощность:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.power_forward = ttk.Combobox(self.crisp_forward_frame, values=["низкая", "средняя", "высокая"])
        self.power_forward.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.crisp_forward_frame, text="Макс. скорость:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.max_speed_forward = ttk.Combobox(self.crisp_forward_frame, values=["низкая", "средняя", "высокая"])
        self.max_speed_forward.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.crisp_forward_frame, text="Клиренс:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.clearance_forward = ttk.Combobox(self.crisp_forward_frame, values=["маленький", "средний", "большой"])
        self.clearance_forward.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.crisp_forward_frame, text="Объем багажника:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.trunk_forward = ttk.Combobox(self.crisp_forward_frame, values=["маленький", "средний", "большой"])
        self.trunk_forward.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.crisp_forward_frame, text="Расход топлива:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.fuel_forward = ttk.Combobox(self.crisp_forward_frame, values=["маленький", "средний", "большой"])
        self.fuel_forward.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.crisp_forward_frame, text="Динамика:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.dynamics_forward = ttk.Combobox(self.crisp_forward_frame, values=["низкая", "средняя", "высокая"])
        self.dynamics_forward.grid(row=5, column=1, padx=5, pady=5)

        # Кнопка выполнения
        ttk.Button(self.crisp_forward_frame, text="Подобрать автомобили",
                   command=self.run_crisp_forward).grid(row=6, column=0, columnspan=2, pady=10)

    def create_crisp_backward_widgets(self):
        # Параметры автомобиля
        ttk.Label(self.crisp_backward_frame, text="Мощность:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.power_backward = ttk.Combobox(self.crisp_backward_frame, values=["низкая", "средняя", "высокая"])
        self.power_backward.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.crisp_backward_frame, text="Макс. скорость:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.max_speed_backward = ttk.Combobox(self.crisp_backward_frame, values=["низкая", "средняя", "высокая"])
        self.max_speed_backward.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.crisp_backward_frame, text="Клиренс:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.clearance_backward = ttk.Combobox(self.crisp_backward_frame, values=["маленький", "средний", "большой"])
        self.clearance_backward.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.crisp_backward_frame, text="Объем багажника:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.trunk_backward = ttk.Combobox(self.crisp_backward_frame, values=["маленький", "средний", "большой"])
        self.trunk_backward.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.crisp_backward_frame, text="Расход топлива:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.fuel_backward = ttk.Combobox(self.crisp_backward_frame, values=["маленький", "средний", "большой"])
        self.fuel_backward.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.crisp_backward_frame, text="Динамика:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.dynamics_backward = ttk.Combobox(self.crisp_backward_frame, values=["низкая", "средняя", "высокая"])
        self.dynamics_backward.grid(row=5, column=1, padx=5, pady=5)

        # Кнопка выполнения
        ttk.Button(self.crisp_backward_frame, text="Подобрать автомобиль",
                   command=self.run_crisp_backward).grid(row=6, column=0, columnspan=2, pady=10)

    def create_fuzzy_widgets(self):
        # Параметры автомобиля
        ttk.Label(self.fuzzy_frame, text="Мощность (1-10):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.power_fuzzy = ttk.Entry(self.fuzzy_frame)
        self.power_fuzzy.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.fuzzy_frame, text="Макс. скорость (1-10):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.max_speed_fuzzy = ttk.Entry(self.fuzzy_frame)
        self.max_speed_fuzzy.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.fuzzy_frame, text="Клиренс (1-10):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.clearance_fuzzy = ttk.Entry(self.fuzzy_frame)
        self.clearance_fuzzy.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.fuzzy_frame, text="Объем багажника (1-10):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.trunk_fuzzy = ttk.Entry(self.fuzzy_frame)
        self.trunk_fuzzy.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.fuzzy_frame, text="Расход топлива (1-10):").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.fuel_fuzzy = ttk.Entry(self.fuzzy_frame)
        self.fuel_fuzzy.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.fuzzy_frame, text="Динамика (1-10):").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.dynamics_fuzzy = ttk.Entry(self.fuzzy_frame)
        self.dynamics_fuzzy.grid(row=5, column=1, padx=5, pady=5)

        # Выбор типа фаззификации
        ttk.Label(self.fuzzy_frame, text="Тип фаззификации:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.fuzz_type = ttk.Combobox(self.fuzzy_frame, values=["Треугольная функция", "Трапециевидная функция", "Функция Гаусса", "Обобщенная функция Гаусса"])
        self.fuzz_type.current(0)
        self.fuzz_type.grid(row=6, column=1, padx=5, pady=5)

        # Выбор типа дефаззификации
        ttk.Label(self.fuzzy_frame, text="Тип дефаззификации:").grid(row=7, column=0, padx=5, pady=5, sticky=tk.W)
        self.defuzz_type = ttk.Combobox(self.fuzzy_frame, values=["Метод центра тяжести", "Относительно среднего максимума", "Максимум степени принадлежности"])
        self.defuzz_type.current(0)
        self.defuzz_type.grid(row=7, column=1, padx=5, pady=5)

        # Кнопка выполнения
        ttk.Button(self.fuzzy_frame, text="Рассчитать бюджет", command=self.run_fuzzy).grid(row=8, column=0, columnspan=2, pady=10)

    def clear_results(self):
        self.result_text.delete(1.0, tk.END)

    def print_result(self, text):
        self.result_text.insert(tk.END, text + "\n")

    def run_crisp_forward(self):
        self.clear_results()

        try:
            power = Power(self.power_forward.get())
            max_speed = MaxSpeed(self.max_speed_forward.get())
            clearance = Clearance(self.clearance_forward.get())
            trunk = TrunkVolume(self.trunk_forward.get())
            fuel = FuelConsumption(self.fuel_forward.get())
            dynamics = Dynamics(self.dynamics_forward.get())
        except ValueError as e:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля корректными значениями")
            return

        inputs = (power, max_speed, clearance, trunk, fuel, dynamics)
        suitable_cars = self.forward_chaining(inputs)

        if suitable_cars:
            self.print_result("\nПодходящие автомобили:")
            for car, matches in suitable_cars:
                self.print_result(f"\n{car.name} (совпадений: {matches}/6):")
                self.print_result(f"- Мощность: {car.power.value} {'✓' if car.power == inputs[0] else '✗'}")
                self.print_result(
                    f"- Макс. скорость: {car.max_speed.value} {'✓' if car.max_speed == inputs[1] else '✗'}")
                self.print_result(f"- Клиренс: {car.clearance.value} {'✓' if car.clearance == inputs[2] else '✗'}")
                self.print_result(
                    f"- Объем багажника: {car.trunk_volume.value} {'✓' if car.trunk_volume == inputs[3] else '✗'}")
                self.print_result(
                    f"- Расход топлива: {car.fuel_consumption.value} {'✓' if car.fuel_consumption == inputs[4] else '✗'}")
                self.print_result(f"- Динамика: {car.dynamics.value} {'✓' if car.dynamics == inputs[5] else '✗'}")
                self.print_result(f"Цена: {car.price:,} руб.")
        else:
            self.print_result("\nПодходящих автомобилей не найдено.")

    def run_crisp_backward(self):
        self.clear_results()

        try:
            power = Power(self.power_backward.get())
            max_speed = MaxSpeed(self.max_speed_backward.get())
            clearance = Clearance(self.clearance_backward.get())
            trunk = TrunkVolume(self.trunk_backward.get())
            fuel = FuelConsumption(self.fuel_backward.get())
            dynamics = Dynamics(self.dynamics_backward.get())
        except ValueError as e:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля корректными значениями")
            return

        inputs = (power, max_speed, clearance, trunk, fuel, dynamics)
        suitable_car = self.backward_chaining(inputs)

        if suitable_car:
            self.print_result(f"\nРекомендуемый автомобиль: {suitable_car.name}")
            self.print_result(f"Цена: {suitable_car.price:,} руб.")
        else:
            self.print_result("\nПодходящих автомобилей не найдено.")

    def run_fuzzy(self):
        self.clear_results()

        try:
            power = float(self.power_fuzzy.get())
            max_speed = float(self.max_speed_fuzzy.get())
            clearance = float(self.clearance_fuzzy.get())
            trunk = float(self.trunk_fuzzy.get())
            fuel = float(self.fuel_fuzzy.get())
            dynamics = float(self.dynamics_fuzzy.get())

            if not all(1 <= x <= 10 for x in [power, max_speed, clearance, trunk, fuel, dynamics]):
                raise ValueError("Значения должны быть от 1 до 10")

        except ValueError as e:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля корректными числовыми значениями от 1 до 10")
            return

        inputs = {
            "мощность": power,
            "макс. скорость": max_speed,
            "клиренс": clearance,
            "объем багажника": trunk,
            "расход топлива": fuel,
            "динамика": dynamics
        }

        fuzzification_type = {
            "Треугольная функция": "triangular",
            "Трапециевидная функция": "trapezoidal",
            "Функция Гаусса": "gaussian",
            "Обобщенная функция Гаусса": "generalized_gaussian"
        }.get(self.fuzz_type.get(), "triangular")

        defuzzification_type = {
            "Метод центра тяжести": "center_of_gravity",
            "Относительно среднего максимума": "mean_of_maximum",
            "Максимум степени принадлежности": "maximum_membership"
        }.get(self.defuzz_type.get(), "center_of_gravity")

        budget_membership, budget = self.fuzzy_inference(inputs, defuzzification_type)

        self.print_result(f"\nПолученный бюджет после дефаззификации: {budget:,.0f} руб.")

        closest_car, diff = self.find_closest_car(budget)
        self.print_result(f"\nРекомендуемый автомобиль (наиболее близкий к бюджету):")
        self.print_result(f"{closest_car.name} ({closest_car.price:,} руб.)")
        self.print_result(f"Разница с бюджетом: {int(diff):,} руб.")

    def forward_chaining(self, inputs: Tuple[Power, MaxSpeed, Clearance, TrunkVolume, FuelConsumption, Dynamics]) -> \
    List[Tuple[CarSpecs, int]]:
        """Прямая цепочка рассуждений для четкой ЭС"""
        power, max_speed, clearance, trunk, fuel, dynamics = inputs
        suitable_cars = []

        for car in cars:
            matches = 0
            total = 6

            if car.power == power:
                matches += 1
            if car.max_speed == max_speed:
                matches += 1
            if car.clearance == clearance:
                matches += 1
            if car.trunk_volume == trunk:
                matches += 1
            if car.fuel_consumption == fuel:
                matches += 1
            if car.dynamics == dynamics:
                matches += 1

            if matches >= 5:  # Минимум 5 из 6 параметров должны совпадать
                suitable_cars.append((car, matches))

        return suitable_cars

    def backward_chaining(self, inputs: Tuple[Power, MaxSpeed, Clearance, TrunkVolume, FuelConsumption, Dynamics]) -> \
    Optional[CarSpecs]:
        """Обратная цепочка рассуждений для четкой ЭС"""
        power, max_speed, clearance, trunk, fuel, dynamics = inputs

        for car in cars:
            self.print_result(f"\nПроверка {car.name}:")
            matches = 0
            total = 6

            # Проверка мощности
            self.print_result(f"- Мощность: {car.power.value} {'✓' if car.power == power else '✗'}")
            if car.power == power:
                matches += 1
            else:
                self.print_result(f"Вариант {car.name} отвергнут.")
                continue

            # Проверка максимальной скорости
            self.print_result(f"- Макс. скорость: {car.max_speed.value} {'✓' if car.max_speed == max_speed else '✗'}")
            if car.max_speed == max_speed:
                matches += 1
            else:
                self.print_result(f"Вариант {car.name} отвергнут.")
                continue

            # Проверка клиренса
            self.print_result(f"- Клиренс: {car.clearance.value} {'✓' if car.clearance == clearance else '✗'}")
            if car.clearance == clearance:
                matches += 1
            else:
                self.print_result(f"Вариант {car.name} отвергнут.")
                continue

            # Проверка объема багажника
            self.print_result(f"- Объем багажника: {car.trunk_volume.value} {'✓' if car.trunk_volume == trunk else '✗'}")
            if car.trunk_volume == trunk:
                matches += 1
            else:
                self.print_result(f"Вариант {car.name} отвергнут.")
                continue

            # Проверка расхода топлива
            self.print_result(f"- Расход топлива: {car.fuel_consumption.value} {'✓' if car.fuel_consumption == fuel else '✗'}")
            if car.fuel_consumption == fuel:
                matches += 1
            else:
                self.print_result(f"Вариант {car.name} отвергнут.")
                continue

            # Проверка динамики
            self.print_result(f"- Динамика: {car.dynamics.value} {'✓' if car.dynamics == dynamics else '✗'}")
            if car.dynamics == dynamics:
                matches += 1
            else:
                self.print_result(f"Вариант {car.name} отвергнут.")
                continue

            # Если все параметры совпали
            self.print_result(f"Вариант {car.name} подходит. Проверка окончена.")
            return car

        return None

    def get_membership_value(self, x: float, param_type: str, param_name: str) -> float:
        """Получение значения функции принадлежности"""
        params = FUZZY_PARAMS[param_type][param_name]
        if params["type"] == "triangular":
            return triangular(x, *params["params"])
        elif params["type"] == "trapezoidal":
            return trapezoidal(x, *params["params"])
        elif params["type"] == "gaussian":
            return gaussian(x, *params["params"])
        elif params["type"] == "generalized_gaussian":
            return generalized_gaussian(x, *params["params"])
        return 0.0

    def get_budget_membership(self, x: float, budget_level: str) -> float:
        """Получение значения функции принадлежности для бюджета"""
        params = BUDGET_PARAMS[budget_level]
        if params["type"] == "triangular":
            return triangular(x, *params["params"])
        elif params["type"] == "trapezoidal":
            return trapezoidal(x, *params["params"])
        elif params["type"] == "gaussian":
            return gaussian(x, *params["params"])
        elif params["type"] == "generalized_gaussian":
            return generalized_gaussian(x, *params["params"])
        return 0.0

    def fuzzy_inference(self, inputs: Dict[str, float], defuzzification_type: str = "center_of_gravity") -> Tuple[Dict[str, float], float]:
        # Фаззификация входных переменных
        membership_values = {}
        self.print_result("\nЗначения функций принадлежности для входных параметров:")
        for param, value in inputs.items():
            membership_values[param] = {}
            self.print_result(f"\n{param} (значение: {value}):")
            for level in ["низкая", "средняя", "высокая"] \
                if param in ["мощность", "макс. скорость", "динамика"] \
                else ["маленький", "средний", "большой"]:
                membership_values[param][level] = self.get_membership_value(value, param, level)
                self.print_result(f"- {level}: {membership_values[param][level]:.3f}")

        # Агрегация правил
        budget_membership = {level: 0.0 for level in Budget}

        self.print_result("\nПрименение правил:")
        for i, rule in enumerate(fuzzy_rules, 1):
            # Вычисление степени истинности правила как среднего значения активаций
            activations = []
            for param, level in rule["if"].items():
                activations.append(membership_values[param][level])

            # Используем среднее значение активаций вместо минимума
            rule_strength = sum(activations) / len(activations)

            # Обновление выходной переменной
            budget_level = rule["then"]["бюджет"]
            budget_membership[budget_level] = max(budget_membership[budget_level], rule_strength)
            self.print_result(f"Правило {i}: {budget_level.value} = {rule_strength:.3f}")

        # Дефаззификация
        x = np.linspace(500000, 9000000, 1000)
        y = np.zeros_like(x)

        self.print_result("\nДефаззификация:")
        for budget_level, membership in budget_membership.items():
            if membership > 0:
                self.print_result(f"{budget_level.value}: {membership:.3f}")
                y += membership * np.array([self.get_budget_membership(xi, budget_level.value) for xi in x])

        if np.sum(y) == 0:
            self.print_result("\nПредупреждение: Все значения функций принадлежности равны нулю!")
            # Возвращаем средний бюджет как запасной вариант
            return budget_membership, 3500000

        if defuzzification_type == "center_of_gravity":
            budget = center_of_gravity(x, y)
        elif defuzzification_type == "mean_of_maximum":
            budget = mean_of_maximum(x, y)
        else:  # maximum_membership
            budget = maximum_membership(x, y)

        return budget_membership, budget

    def find_closest_car(self, budget: float) -> Tuple[CarSpecs, float]:
        """Поиск автомобиля с наиболее близкой ценой к бюджету"""
        closest_car = min(cars, key=lambda car: abs(car.price - budget))
        return closest_car, abs(closest_car.price - budget)

def main():
    root = tk.Tk()
    app = CarExpertSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()