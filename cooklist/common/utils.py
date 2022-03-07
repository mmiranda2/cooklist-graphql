class stringmod:
    @classmethod
    def standard_section(cls, section):
        '''Standard section heading capitalized and within 2 newlines'''
        mod = cls.string_mod(begin='\n', end='\n', func=lambda s: s.capitalize())
        return mod(s)
    
    @classmethod
    def bad_section_colon(cls, section):
        '''Section heading capitalized, colonized, and within 2 newlines'''
        mod = cls.string_mod(end=':')
        return cls.standard_section(mod(s))
    
    @staticmethod
    def string_mod(begin='', end='', func=lambda x: x):
        return lambda s: begin + func(s) + end
