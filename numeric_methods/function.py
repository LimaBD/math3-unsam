#! /usr/bin/env python
#
# Function module
#
## TODO: ensure that function is not empty.
##       pretty verbose print.
#
# by Bruno Daniel Lima, in collaboration with
# Nahuel Carron, Felipe Carballo and Federico Marquez.


"""Function module"""


# Standard packages
import re
import math


# Local packages
import error as err


class Function:
    """Function main class"""


    # Global
    _function = ''
    _verbose  = False


    def __init__(self, new_function='', verbose=False):
        self.set_function(new_function)
        self.set_verbose(verbose)


    def set_verbose(self, new_bool):
        """Set to output verbose"""
        self._verbose = new_bool


    def set_function(self, new_function):
        """Set function string"""
        self._function = new_function.lower()


    def get_function(self):
        """Returns function string"""
        return self._function


    def get_formated_function(self):
        """Convert function to an executable string"""
        result = self._function
        ## TODO: format x^(3*x*2) => (x**(3*x*2))
        ## TODO: format sin, cos, tan
        ## TODO: format divisions
        result = re.sub(r'([0-9]+)([a-zA-Z]+)', r'\1*\2', result) # 2x => 2*x
        result = re.sub(r'(\w+\^\w+)', r'(\1)', result)           # x^3 => (x^3)
        result = re.sub(r'\^', r'**', result)                     # x^5 => x**5
        return result


    # pylint: disable=invalid-name, unused-argument, eval-used
    def calc(self, x):
        """Calculate function"""
        ## TODO: implement usage of multiples values, not just x.
        return eval(self.get_formated_function())


    def bolsano_signs_condition(self, interval):
        """Check Bolsano theorem condition:
           on interval [a, b] and a continuous f(),
           if f(a) and f(b) has different signs on some
           point between a and b should be an root"""
        return self.calc(interval[0]) * self.calc(interval[-1]) < 0


    # pylint: disable=no-self-use
    def calc_bolsano_steps(self, interval, error, splits):
        """Calculate number of steps to approximate the interval to an root
           using the Bolsano theorem"""
        result = math.log( abs(interval[-1] - interval[0]) / error, splits)
        result = int(math.ceil(result))
        return result


    def nsection(self, interval, error, splits=2, max_steps=0):
        """Get root of function using Bolsano theorem,
           this function is very flexible, SPLITS could be an integer
           or an array, you can specify number of MAX_STEPS to terminate
           the loop"""

        # Check interval
        assert len(interval) >= 2, 'interval must containt at least 2 values.'
        assert self.bolsano_signs_condition(interval), f'no roots in {interval} according to Bolsano theorem.'
        a_value, b_value = interval[0], interval[-1]

        # Check error
        assert error > 0, 'error must be higher than 0 (zero)'

        # Check splits
        assert (isinstance(splits, list) or (isinstance(splits, int) and splits > 0)),'wrong splits'
        max_splits = max(splits) if isinstance(splits, list) else splits

        # Check max steps
        assert isinstance(max_steps, int), 'max_steps must be an int.'
        assert max_steps >= 0, 'max number of steps must be higher or equal to 0 (zero)'

        root = None
        step = segments = 0
        verbose_text  = ''
        current_error = 0.0

        while True:
            # Get number of splits
            n_splits = get_correlative(splits, step) if isinstance(splits, list) else splits

            # Calculate segment
            segment_len = (b_value - a_value) / n_splits
            a_temp = a_value + segment_len * segments
            b_temp = a_value + segment_len * (segments + 1)

            # Verbose
            ## TODO: remove inaccurated decimals.
            current_error = round(err.absolute_error([a_temp, b_temp]), len(str(error)))
            if segments == 0:
                verbose_text = f'step={step}\t{self._function_string(a_temp, current_error)}'
            verbose_text += f'\t{self._function_string(b_temp, current_error)}'

            # Root conditions
            if self.calc(b_temp) == 0:
                root = b_temp
                if self._verbose:
                    print('root founded.')
                break
            if self.bolsano_signs_condition([a_temp, b_temp]):
                a_value = a_temp
                b_value = b_temp

                if self._verbose:
                    ## TODO: remove inaccurated decimals.
                    verbose_text += ('\t' + '-' * 3).ljust(25, " ") * (max_splits - segments - 1)
                    verbose_text += f'\troot={str(err.remove_inaccuracy((a_value + b_value)/2, current_error)).ljust(25, " ")}'
                    verbose_text += f'\terror={round(current_error, len(str(error)))}'
                    print(verbose_text)

                step    += 1
                segments = 0
            else:
                segments += 1

            # Stop conditions
            if b_value - a_value < error:
                if self._verbose:
                    print('reached acceptable error.')
                break
            if step > self.calc_bolsano_steps(interval, error, max_splits):
                if self._verbose:
                    print('reached expected number of steps.')
                break
            if 0 < max_steps <= step:
                if self._verbose:
                    print('reached specified number of steps.')
                break

        # If the exact root is not founded, get the middle value
        root = root if root else (a_value + b_value) / 2

        # Remove inaccurated decimals
        root = err.remove_inaccuracy(root, current_error)

        return root, current_error


    # pylint: disable=invalid-name
    def _function_string(self, value, error=1, ljust=25):
        """Returns function string"""
        return f'f({err.remove_inaccuracy(value, error)})={err.remove_inaccuracy(self.calc(value), error)}'.ljust(ljust, ' ')


    def bisection(self, interval, error):
        """Get root of function using Bolsano theorem,
           cutting the interval by 2 for each step"""
        return self.nsection(interval, error, splits=2)


    def trisection(self, interval, error):
        """Get root of function using Bolsano theorem,
           cutting the interval by 3 for each step"""
        return self.nsection(interval, error, splits=3)


def get_correlative(vector, index):
    """Get correlative item in vector,
       e.g. get_correlative([3, 45, 6], 11) => 6"""
    return vector[index % len(vector)]
