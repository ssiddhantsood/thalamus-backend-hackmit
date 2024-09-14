import math
from typing import List, Union, Tuple, Dict, Any, Annotated, Literal



Operator = Literal["+", "-", "*", "/"]

def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")

class MathToolkit:
    @staticmethod
    def geometry(operation: str, *args) -> Union[float, Tuple[float, float, float]]:
        """
        Perform various geometry calculations.
        
        Operations:
        - triangle_area: base, height
        - triangle_area_sides: a, b, c (Heron's formula)
        - triangle_area_trig: a, b, angle (in radians)
        - square_area: side
        - rectangle_area: length, width
        - trapezoid_area: b1, b2, height
        - regular_hexagon_area: side
        - regular_polygon_area: n (number of sides), side
        - circle_area: radius
        - sphere_volume: radius
        - sphere_surface_area: radius
        - cone_volume: radius, height
        - cone_surface_area: radius, slant_height
        - cylinder_volume: radius, height
        - cylinder_surface_area: radius, height
        - pyramid_volume: base_area, height
        - pyramid_surface_area: base_perimeter, slant_height, base_area
        - pythagorean: a, b (returns c)
        - distance: x1, y1, x2, y2
        - quadratic_roots: a, b, c (for ax^2 + bx + c = 0)
        - arithmetic_series_sum: first_term, last_term, num_terms
        - geometric_series_sum: first_term, ratio, num_terms
        - infinite_geometric_series_sum: first_term, ratio (|ratio| < 1)
        - logarithm: base, argument
        - exponent: base, power
        - factorial: n
        - permutation: n, r
        - combination: n, r
        - binomial_theorem: a, b, n
        - vieta_quadratic: a, b, c (returns sum and product of roots)
        """
        if operation == "triangle_area":
            return 0.5 * args[0] * args[1]
        elif operation == "triangle_area_sides":
            s = sum(args) / 2
            return math.sqrt(s * (s - args[0]) * (s - args[1]) * (s - args[2]))
        elif operation == "triangle_area_trig":
            return 0.5 * args[0] * args[1] * math.sin(args[2])
        elif operation == "square_area":
            return args[0] ** 2
        elif operation == "rectangle_area":
            return args[0] * args[1]
        elif operation == "trapezoid_area":
            return 0.5 * (args[0] + args[1]) * args[2]
        elif operation == "regular_hexagon_area":
            return 3 * math.sqrt(3) * args[0] ** 2 / 2
        elif operation == "regular_polygon_area":
            n, s = args
            return (n * s ** 2) / (4 * math.tan(math.pi / n))
        elif operation == "circle_area":
            return math.pi * args[0] ** 2
        elif operation == "sphere_volume":
            return (4/3) * math.pi * args[0] ** 3
        elif operation == "sphere_surface_area":
            return 4 * math.pi * args[0] ** 2
        elif operation == "cone_volume":
            return math.pi * args[0] ** 2 * args[1] / 3
        elif operation == "cone_surface_area":
            return math.pi * args[0] * (args[0] + args[1])
        elif operation == "cylinder_volume":
            return math.pi * args[0] ** 2 * args[1]
        elif operation == "cylinder_surface_area":
            return 2 * math.pi * args[0] * (args[0] + args[1])
        elif operation == "pyramid_volume":
            return args[0] * args[1] / 3
        elif operation == "pyramid_surface_area":
            return args[0] * args[1] / 2 + args[2]
        elif operation == "pythagorean":
            return math.sqrt(args[0] ** 2 + args[1] ** 2)
        elif operation == "distance":
            return math.sqrt((args[2] - args[0]) ** 2 + (args[3] - args[1]) ** 2)
        

    @staticmethod
    def algebra(operation: str, *args) -> Union[float, Tuple[float, float], List[float]]:
        """
        Perform various algebraic calculations.
        
        Operations:
        - 
        """
        if operation == "quadratic_roots":
            a, b, c = args
            discriminant = b ** 2 - 4 * a * c
            if discriminant > 0:
                return (-b + math.sqrt(discriminant)) / (2 * a), (-b - math.sqrt(discriminant)) / (2 * a)
            elif discriminant == 0:
                return -b / (2 * a),
            else:
                return []
        elif operation == "arithmetic_series_sum":
            return (args[2] / 2) * (args[0] + args[1])
        elif operation == "geometric_series_sum":
            if args[1] == 1:
                return args[0] * args[2]
            return args[0] * (1 - args[1] ** args[2]) / (1 - args[1])
        elif operation == "infinite_geometric_series_sum":
            if abs(args[1]) >= 1:
                raise ValueError("Ratio must be less than 1 for infinite series")
            return args[0] / (1 - args[1])
        elif operation == "logarithm":
            return math.log(args[1], args[0])
        elif operation == "exponent":
            return args[0] ** args[1]
        elif operation == "factorial":
            return math.factorial(args[0])
        elif operation == "permutation":
            return math.factorial(args[0]) // math.factorial(args[0] - args[1])
        elif operation == "combination":
            return math.factorial(args[0]) // (math.factorial(args[1]) * math.factorial(args[0] - args[1]))
        elif operation == "binomial_theorem":
            a, b, n = args
            return sum(MathToolkit.algebra("combination", n, k)[0] * (a ** (n-k)) * (b ** k) for k in range(n+1))
        elif operation == "vieta_quadratic":
            a, b, c = args
            return -b/a, c/a  # sum of roots, product of roots
        else:
            raise ValueError("Invalid algebra operation")

    @staticmethod
    def number_theory(operation: str, *args) -> Union[int, bool, List[int]]:
        """
        Perform various number theory calculations.
        
        Operations:
        - is_prime: n
        - prime_factors: n
        - gcd: a, b
        - lcm: a, b
        - euler_totient: n
        - modular_exponentiation: base, exponent, modulus
        - chinese_remainder_theorem: remainders, moduli
        """
        if operation == "is_prime":
            n = args[0]
            if n < 2:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True
        elif operation == "prime_factors":
            n = args[0]
            factors = []
            d = 2
            while n > 1:
                while n % d == 0:
                    factors.append(d)
                    n //= d
                d += 1
                if d * d > n:
                    if n > 1:
                        factors.append(n)
                    break
            return factors
        elif operation == "gcd":
            a, b = args
            while b:
                a, b = b, a % b
            return a
        elif operation == "lcm":
            a, b = args
            return abs(a * b) // MathToolkit.number_theory("gcd", a, b)
        elif operation == "euler_totient":
            n = args[0]
            result = n
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    while n % i == 0:
                        n //= i
                    result *= (1 - 1/i)
            if n > 1:
                result *= (1 - 1/n)
            return int(result)
        elif operation == "modular_exponentiation":
            base, exponent, modulus = args
            result = 1
            base = base % modulus
            while exponent > 0:
                if exponent % 2 == 1:
                    result = (result * base) % modulus
                exponent = exponent >> 1
                base = (base * base) % modulus
            return result
        elif operation == "chinese_remainder_theorem":
            remainders, moduli = args
            total = 0
            product = math.prod(moduli)
            for remainder, modulus in zip(remainders, moduli):
                p = product // modulus
                total += remainder * MathToolkit.number_theory("modular_exponentiation", p, MathToolkit.number_theory("euler_totient", modulus) - 1, modulus) * p
            return total % product
        else:
            raise ValueError("Invalid number theory operation")

    @staticmethod
    def trigonometry(operation: str, *args) -> Union[float, Tuple[float, float, float]]:
        """
        Perform various trigonometric calculations.
        
        Operations:
        - sin_cos_tan: angle (in radians)
        - law_of_sines: a, A, B (side a, angle A, angle B in radians)
        - law_of_cosines: a, b, C (sides a, b, angle C in radians)
        """
        if operation == "sin_cos_tan":
            angle = args[0]
            return math.sin(angle), math.cos(angle), math.tan(angle)
        elif operation == "law_of_sines":
            a, A, B = args
            return a * math.sin(B) / math.sin(A)
        elif operation == "law_of_cosines":
            a, b, C = args
            return math.sqrt(a**2 + b**2 - 2*a*b*math.cos(C))
        else:
            raise ValueError("Invalid trigonometry operation")

    @staticmethod
    def statistics(operation: str, data: List[float]) -> float:
        """
        Perform various statistical calculations.
        
        Operations:
        - mean
        - median
        - mode
        - range
        - variance
        - standard_deviation
        """
        if operation == "mean":
            return sum(data) / len(data)
        elif operation == "median":
            sorted_data = sorted(data)
            n = len(sorted_data)
            if n % 2 == 0:
                return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
            else:
                return sorted_data[n//2]
        elif operation == "mode":
            return max(set(data), key=data.count)
        elif operation == "range":
            return max(data) - min(data)
        elif operation == "variance":
            mean = MathToolkit.statistics("mean", data)
            return sum((x - mean) ** 2 for x in data) / len(data)
        elif operation == "standard_deviation":
            return math.sqrt(MathToolkit.statistics("variance", data))
        else:
            raise ValueError("Invalid statistics operation")

    @staticmethod
    def probability(operation: str, *args) -> Union[float, int]:
        """
        Perform various probability calculations.
        
        Operations:
        - binomial_probability: n, k, p (n trials, k successes, probability p)
        - expected_value: values, probabilities
        """
        if operation == "binomial_probability":
            n, k, p = args
            return MathToolkit.algebra("combination", n, k) * (p ** k) * ((1 - p) ** (n - k))
        elif operation == "expected_value":
            values, probabilities = args
            return sum(v * p for v, p in zip(values, probabilities))
        else:
            raise ValueError("Invalid probability operation")


def geometry_calculator(operation: str, param1: float, param2: float, param3: float = 0) -> float:
    return MathToolkit.geometry(operation, param1, param2, param3)

def algebra_calculator(operation: str, param1: float, param2: float, param3: float = 0) -> Union[float, Tuple[float, float]]:
    return MathToolkit.algebra(operation, param1, param2, param3)

def number_theory_calculator(operation: str, param1: int, param2: int = 0) -> Union[int, bool, List[int]]:
    return MathToolkit.number_theory(operation, param1, param2)

def trigonometry_calculator(operation: str, param1: float, param2: float = 0, param3: float = 0) -> Union[float, Tuple[float, float, float]]:
    return MathToolkit.trigonometry(operation, param1, param2, param3)

def statistics_calculator(operation: str, data: List[float]) -> float:
    return MathToolkit.statistics(operation, data)

def probability_calculator(operation: str, param1: float, param2: float, param3: float = 0) -> float:
    return MathToolkit.probability(operation, param1, param2, param3)

def unified_calculator(category: str, operation: str, params: Dict[str, Any]) -> Any:
    if category == "geometry":
        return geometry_calculator(operation, params.get('param1', 0), params.get('param2', 0), params.get('param3', 0))
    elif category == "algebra":
        return algebra_calculator(operation, params.get('param1', 0), params.get('param2', 0), params.get('param3', 0))
    elif category == "number_theory":
        return number_theory_calculator(operation, params.get('param1', 0), params.get('param2', 0))
    elif category == "trigonometry":
        return trigonometry_calculator(operation, params.get('param1', 0), params.get('param2', 0), params.get('param3', 0))
    elif category == "statistics":
        return statistics_calculator(operation, params.get('data', []))
    elif category == "probability":
        return probability_calculator(operation, params.get('param1', 0), params.get('param2', 0), params.get('param3', 0))
    else:
        raise ValueError(f"Unknown category: {category}")
# Example usage
if __name__ == "__main__":
    '''
    print(geometry_calculator("triangle_area", 5, 3))  # Output: 7.5
    print(algebra_calculator("quadratic_roots", 1, 5, 6))  # Output: (-2.0, -3.0)
    print(MathToolkit.number_theory("is_prime", 17))  # Output: True
    print(MathToolkit.trigonometry("sin_cos_tan", math.pi/4))  # Output: (0.7071067811865475, 0.7071067811865476, 0.9999999999999999)
    print(MathToolkit.statistics("mean", [1, 2, 3, 4, 5]))  # Output: 3.0
    print(MathToolkit.probability("binomial_probability", 10, 3, 0.5))  # Output: 0.11718750000000001
    '''
