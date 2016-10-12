#!/usr/bin/env python2

import ply.lex as lex
import ply.yacc as yacc
from .model import *
from modules import common

class MyLexer(object):

    keywords = ('this', 'class', 'void', 'super', 'extends', 'implements', 'enum', 'interface',
                'byte', 'short', 'int', 'long', 'char', 'float', 'double', 'boolean', 'null',
                'true', 'false',
                'final', 'public', 'protected', 'private', 'abstract', 'static', 'strictfp', 'transient', 'volatile',
                'synchronized', 'native',
                'throws', 'default',
                'instanceof',
                'if', 'else', 'while', 'for', 'switch', 'case', 'assert', 'do',
                'break', 'continue', 'return', 'throw', 'try', 'catch', 'finally', 'new',
                'package', 'import'
    )

    tokens = [
        'NAME',
        'NUM',
        'CHAR_LITERAL',
        'STRING_LITERAL',
        'LINE_COMMENT', 'BLOCK_COMMENT',

        'OR', 'AND',
        'EQ', 'NEQ', 'GTEQ', 'LTEQ',
        'LSHIFT', 'RSHIFT', 'RRSHIFT',

        'TIMES_ASSIGN', 'DIVIDE_ASSIGN', 'REMAINDER_ASSIGN',
        'PLUS_ASSIGN', 'MINUS_ASSIGN', 'LSHIFT_ASSIGN', 'RSHIFT_ASSIGN', 'RRSHIFT_ASSIGN',
        'AND_ASSIGN', 'OR_ASSIGN', 'XOR_ASSIGN',

        'PLUSPLUS', 'MINUSMINUS',

        'ELLIPSIS'
    ] + [k.upper() for k in keywords]
    literals = '()+-*/=?:,.^|&~!=[]{};<>@%'

    t_NUM = r'\.?[0-9][0-9eE_lLdDa-fA-F.xXpP]*'
    t_CHAR_LITERAL = r'\'([^\\\n]|(\\.))*?\''
    t_STRING_LITERAL = r'\"([^\\\n]|(\\.))*?\"'

    t_ignore_LINE_COMMENT = '//.*'

    def t_BLOCK_COMMENT(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')

    t_OR = r'\|\|'
    t_AND = '&&'

    t_EQ = '=='
    t_NEQ = '!='
    t_GTEQ = '>='
    t_LTEQ = '<='

    t_LSHIFT = '<<'
    t_RSHIFT = '>>'
    t_RRSHIFT = '>>>'

    t_TIMES_ASSIGN = r'\*='
    t_DIVIDE_ASSIGN = '/='
    t_REMAINDER_ASSIGN = '%='
    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = '-='
    t_LSHIFT_ASSIGN = '<<='
    t_RSHIFT_ASSIGN = '>>='
    t_RRSHIFT_ASSIGN = '>>>='
    t_AND_ASSIGN = '&='
    t_OR_ASSIGN = r'\|='
    t_XOR_ASSIGN = '\^='

    t_PLUSPLUS = r'\+\+'
    t_MINUSMINUS = r'\-\-'

    t_ELLIPSIS = r'\.\.\.'

    t_ignore = ' \t\f'

    def t_NAME(self, t):
        '[A-Za-z_$][A-Za-z0-9_$]*'
        if t.value in MyLexer.keywords:
            t.type = t.value.upper()
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_newline2(self, t):
        r'(\r\n)+'
        t.lexer.lineno += len(t.value) / 2

    def t_error(self, t):
        print("Illegal character '{}' ({}) in line {}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
        t.lexer.skip(1)

class ExpressionParser(object):

    def p_expression(self, p):
        '''expression : assignment_expression'''
        p[0] = p[1]

    def p_expression_not_name(self, p):
        '''expression_not_name : assignment_expression_not_name'''
        p[0] = p[1]

    def p_assignment_expression(self, p):
        '''assignment_expression : assignment
                                 | conditional_expression'''
        p[0] = p[1]

    def p_assignment_expression_not_name(self, p):
        '''assignment_expression_not_name : assignment
                                          | conditional_expression_not_name'''
        p[0] = p[1]

    def p_assignment(self, p):
        '''assignment : postfix_expression assignment_operator assignment_expression'''
        p[0] = Assignment(p[2], p[1], p[3])

    def p_assignment_operator(self, p):
        '''assignment_operator : '='
                               | TIMES_ASSIGN
                               | DIVIDE_ASSIGN
                               | REMAINDER_ASSIGN
                               | PLUS_ASSIGN
                               | MINUS_ASSIGN
                               | LSHIFT_ASSIGN
                               | RSHIFT_ASSIGN
                               | RRSHIFT_ASSIGN
                               | AND_ASSIGN
                               | OR_ASSIGN
                               | XOR_ASSIGN'''
        p[0] = p[1]

    def p_conditional_expression(self, p):
        '''conditional_expression : conditional_or_expression
                                  | conditional_or_expression '?' expression ':' conditional_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Conditional(p[1], p[3], p[5])

    def p_conditional_expression_not_name(self, p):
        '''conditional_expression_not_name : conditional_or_expression_not_name
                                           | conditional_or_expression_not_name '?' expression ':' conditional_expression
                                           | name '?' expression ':' conditional_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Conditional(p[1], p[3], p[5])

    def binop(self, p, ctor):
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ctor(p[2], p[1], p[3])

    def p_conditional_or_expression(self, p):
        '''conditional_or_expression : conditional_and_expression
                                     | conditional_or_expression OR conditional_and_expression'''
        self.binop(p, ConditionalOr)

    def p_conditional_or_expression_not_name(self, p):
        '''conditional_or_expression_not_name : conditional_and_expression_not_name
                                              | conditional_or_expression_not_name OR conditional_and_expression
                                              | name OR conditional_and_expression'''
        self.binop(p, ConditionalOr)

    def p_conditional_and_expression(self, p):
        '''conditional_and_expression : inclusive_or_expression
                                      | conditional_and_expression AND inclusive_or_expression'''
        self.binop(p, ConditionalAnd)

    def p_conditional_and_expression_not_name(self, p):
        '''conditional_and_expression_not_name : inclusive_or_expression_not_name
                                               | conditional_and_expression_not_name AND inclusive_or_expression
                                               | name AND inclusive_or_expression'''
        self.binop(p, ConditionalAnd)

    def p_inclusive_or_expression(self, p):
        '''inclusive_or_expression : exclusive_or_expression
                                   | inclusive_or_expression '|' exclusive_or_expression'''
        self.binop(p, Or)

    def p_inclusive_or_expression_not_name(self, p):
        '''inclusive_or_expression_not_name : exclusive_or_expression_not_name
                                            | inclusive_or_expression_not_name '|' exclusive_or_expression
                                            | name '|' exclusive_or_expression'''
        self.binop(p, Or)

    def p_exclusive_or_expression(self, p):
        '''exclusive_or_expression : and_expression
                                   | exclusive_or_expression '^' and_expression'''
        self.binop(p, Xor)

    def p_exclusive_or_expression_not_name(self, p):
        '''exclusive_or_expression_not_name : and_expression_not_name
                                            | exclusive_or_expression_not_name '^' and_expression
                                            | name '^' and_expression'''
        self.binop(p, Xor)

    def p_and_expression(self, p):
        '''and_expression : equality_expression
                          | and_expression '&' equality_expression'''
        self.binop(p, And)

    def p_and_expression_not_name(self, p):
        '''and_expression_not_name : equality_expression_not_name
                                   | and_expression_not_name '&' equality_expression
                                   | name '&' equality_expression'''
        self.binop(p, And)

    def p_equality_expression(self, p):
        '''equality_expression : instanceof_expression
                               | equality_expression EQ instanceof_expression
                               | equality_expression NEQ instanceof_expression'''
        self.binop(p, Equality)

    def p_equality_expression_not_name(self, p):
        '''equality_expression_not_name : instanceof_expression_not_name
                                        | equality_expression_not_name EQ instanceof_expression
                                        | name EQ instanceof_expression
                                        | equality_expression_not_name NEQ instanceof_expression
                                        | name NEQ instanceof_expression'''
        self.binop(p, Equality)

    def p_instanceof_expression(self, p):
        '''instanceof_expression : relational_expression
                                 | instanceof_expression INSTANCEOF reference_type'''
        self.binop(p, InstanceOf)

    def p_instanceof_expression_not_name(self, p):
        '''instanceof_expression_not_name : relational_expression_not_name
                                          | name INSTANCEOF reference_type
                                          | instanceof_expression_not_name INSTANCEOF reference_type'''
        self.binop(p, InstanceOf)

    def p_relational_expression(self, p):
        '''relational_expression : shift_expression
                                 | relational_expression '>' shift_expression
                                 | relational_expression '<' shift_expression
                                 | relational_expression GTEQ shift_expression
                                 | relational_expression LTEQ shift_expression'''
        self.binop(p, Relational)

    def p_relational_expression_not_name(self, p):
        '''relational_expression_not_name : shift_expression_not_name
                                          | shift_expression_not_name '<' shift_expression
                                          | name '<' shift_expression
                                          | shift_expression_not_name '>' shift_expression
                                          | name '>' shift_expression
                                          | shift_expression_not_name GTEQ shift_expression
                                          | name GTEQ shift_expression
                                          | shift_expression_not_name LTEQ shift_expression
                                          | name LTEQ shift_expression'''
        self.binop(p, Relational)

    def p_shift_expression(self, p):
        '''shift_expression : additive_expression
                            | shift_expression LSHIFT additive_expression
                            | shift_expression RSHIFT additive_expression
                            | shift_expression RRSHIFT additive_expression'''
        self.binop(p, Shift)

    def p_shift_expression_not_name(self, p):
        '''shift_expression_not_name : additive_expression_not_name
                                     | shift_expression_not_name LSHIFT additive_expression
                                     | name LSHIFT additive_expression
                                     | shift_expression_not_name RSHIFT additive_expression
                                     | name RSHIFT additive_expression
                                     | shift_expression_not_name RRSHIFT additive_expression
                                     | name RRSHIFT additive_expression'''
        self.binop(p, Shift)

    def p_additive_expression(self, p):
        '''additive_expression : multiplicative_expression
                               | additive_expression '+' multiplicative_expression
                               | additive_expression '-' multiplicative_expression'''
        self.binop(p, Additive)

    def p_additive_expression_not_name(self, p):
        '''additive_expression_not_name : multiplicative_expression_not_name
                                        | additive_expression_not_name '+' multiplicative_expression
                                        | name '+' multiplicative_expression
                                        | additive_expression_not_name '-' multiplicative_expression
                                        | name '-' multiplicative_expression'''
        self.binop(p, Additive)

    def p_multiplicative_expression(self, p):
        '''multiplicative_expression : unary_expression
                                     | multiplicative_expression '*' unary_expression
                                     | multiplicative_expression '/' unary_expression
                                     | multiplicative_expression '%' unary_expression'''
        self.binop(p, Multiplicative)

    def p_multiplicative_expression_not_name(self, p):
        '''multiplicative_expression_not_name : unary_expression_not_name
                                              | multiplicative_expression_not_name '*' unary_expression
                                              | name '*' unary_expression
                                              | multiplicative_expression_not_name '/' unary_expression
                                              | name '/' unary_expression
                                              | multiplicative_expression_not_name '%' unary_expression
                                              | name '%' unary_expression'''
        self.binop(p, Multiplicative)

    def p_unary_expression(self, p):
        '''unary_expression : pre_increment_expression
                            | pre_decrement_expression
                            | '+' unary_expression
                            | '-' unary_expression
                            | unary_expression_not_plus_minus'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])

    def p_unary_expression_not_name(self, p):
        '''unary_expression_not_name : pre_increment_expression
                                     | pre_decrement_expression
                                     | '+' unary_expression
                                     | '-' unary_expression
                                     | unary_expression_not_plus_minus_not_name'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])

    def p_pre_increment_expression(self, p):
        '''pre_increment_expression : PLUSPLUS unary_expression'''
        p[0] = Unary('++x', p[2])

    def p_pre_decrement_expression(self, p):
        '''pre_decrement_expression : MINUSMINUS unary_expression'''
        p[0] = Unary('--x', p[2])

    def p_unary_expression_not_plus_minus(self, p):
        '''unary_expression_not_plus_minus : postfix_expression
                                           | '~' unary_expression
                                           | '!' unary_expression
                                           | cast_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])

    def p_unary_expression_not_plus_minus_not_name(self, p):
        '''unary_expression_not_plus_minus_not_name : postfix_expression_not_name
                                                    | '~' unary_expression
                                                    | '!' unary_expression
                                                    | cast_expression'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = Unary(p[1], p[2])

    def p_postfix_expression(self, p):
        '''postfix_expression : primary
                              | name
                              | post_increment_expression
                              | post_decrement_expression'''
        p[0] = p[1]

    def p_postfix_expression_not_name(self, p):
        '''postfix_expression_not_name : primary
                                       | post_increment_expression
                                       | post_decrement_expression'''
        p[0] = p[1]

    def p_post_increment_expression(self, p):
        '''post_increment_expression : postfix_expression PLUSPLUS'''
        p[0] = Unary('x++', p[1])

    def p_post_decrement_expression(self, p):
        '''post_decrement_expression : postfix_expression MINUSMINUS'''
        p[0] = Unary('x--', p[1])

    def p_primary(self, p):
        '''primary : primary_no_new_array
                   | array_creation_with_array_initializer
                   | array_creation_without_array_initializer'''
        p[0] = p[1]

    def p_primary_no_new_array(self, p):
        '''primary_no_new_array : literal
                                | THIS
                                | class_instance_creation_expression
                                | field_access
                                | method_invocation
                                | array_access'''
        p[0] = p[1]

    def p_primary_no_new_array2(self, p):
        '''primary_no_new_array : '(' name ')'
                                | '(' expression_not_name ')' '''
        p[0] = p[2]

    def p_primary_no_new_array3(self, p):
        '''primary_no_new_array : name '.' THIS
                                | name '.' SUPER'''
        p[1].append_name(p[3])
        p[0] = p[1]

    def p_primary_no_new_array4(self, p):
        '''primary_no_new_array : name '.' CLASS
                                | name dims '.' CLASS
                                | primitive_type dims '.' CLASS
                                | primitive_type '.' CLASS'''
        if len(p) == 4:
            p[0] = ClassLiteral(Type(p[1]))
        else:
            p[0] = ClassLiteral(Type(p[1], dimensions=p[2]))

    def p_dims_opt(self, p):
        '''dims_opt : dims'''
        p[0] = p[1]

    def p_dims_opt2(self, p):
        '''dims_opt : empty'''
        p[0] = 0

    def p_dims(self, p):
        '''dims : dims_loop'''
        p[0] = p[1]

    def p_dims_loop(self, p):
        '''dims_loop : one_dim_loop
                     | dims_loop one_dim_loop'''
        if len(p) == 2:
            p[0] = 1
        else:
            p[0] = 1 + p[1]

    def p_one_dim_loop(self, p):
        '''one_dim_loop : '[' ']' '''
        # ignore

    def p_cast_expression(self, p):
        '''cast_expression : '(' primitive_type dims_opt ')' unary_expression'''
        p[0] = Cast(Type(p[2], dimensions=p[3]), p[5])

    def p_cast_expression2(self, p):
        '''cast_expression : '(' name type_arguments dims_opt ')' unary_expression_not_plus_minus'''
        p[0] = Cast(Type(p[2], type_arguments=p[3], dimensions=p[4]), p[6])

    def p_cast_expression3(self, p):
        '''cast_expression : '(' name type_arguments '.' class_or_interface_type dims_opt ')' unary_expression_not_plus_minus'''
        p[5].dimensions = p[6]
        p[5].enclosed_in = Type(p[2], type_arguments=p[3])
        p[0] = Cast(p[5], p[8])

    def p_cast_expression4(self, p):
        '''cast_expression : '(' name ')' unary_expression_not_plus_minus'''
        # technically it's not necessarily a type but could be a type parameter
        p[0] = Cast(Type(p[2]), p[4])

    def p_cast_expression5(self, p):
        '''cast_expression : '(' name dims ')' unary_expression_not_plus_minus'''
        # technically it's not necessarily a type but could be a type parameter
        p[0] = Cast(Type(p[2], dimensions=p[3]), p[5])

class StatementParser(object):
	
    def p_block(self, p):
        '''block : '{' block_statements_opt '}' '''
        p[0] = Block(p[2])

    def p_block_statements_opt(self, p):
        '''block_statements_opt : block_statements'''
        p[0] = p[1]

    def p_block_statements_opt2(self, p):
        '''block_statements_opt : empty'''
        p[0] = []

    def p_block_statements(self, p):
        '''block_statements : block_statement
                            | block_statements block_statement'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_block_statement(self, p):
        '''block_statement : local_variable_declaration_statement
                           | statement
                           | class_declaration
                           | interface_declaration
                           | annotation_type_declaration
                           | enum_declaration'''
        p[0] = p[1]

    def p_local_variable_declaration_statement(self, p):
        '''local_variable_declaration_statement : local_variable_declaration ';' '''
        p[0] = p[1]

    def p_local_variable_declaration(self, p):
        '''local_variable_declaration : type variable_declarators'''
        p[0] = VariableDeclaration(p[1], p[2])

    def p_local_variable_declaration2(self, p):
        '''local_variable_declaration : modifiers type variable_declarators'''
        p[0] = VariableDeclaration(p[2], p[3], modifiers=p[1])

    def p_variable_declarators(self, p):
        '''variable_declarators : variable_declarator
                                | variable_declarators ',' variable_declarator'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_variable_declarator(self, p):
        '''variable_declarator : variable_declarator_id
                               | variable_declarator_id '=' variable_initializer'''
        if len(p) == 2:
            p[0] = VariableDeclarator(p[1])
        else:
            p[0] = VariableDeclarator(p[1], initializer=p[3])

    def p_variable_declarator_id(self, p):
        '''variable_declarator_id : NAME dims_opt'''
        p[0] = Variable(p[1], dimensions=p[2])

    def p_variable_initializer(self, p):
        '''variable_initializer : expression
                                | array_initializer'''
        p[0] = p[1]

    def p_statement(self, p):
        '''statement : statement_without_trailing_substatement
                     | labeled_statement
                     | if_then_statement
                     | if_then_else_statement
                     | while_statement
                     | for_statement
                     | enhanced_for_statement'''
        p[0] = p[1]

    def p_statement_without_trailing_substatement(self, p):
        '''statement_without_trailing_substatement : block
                                                   | expression_statement
                                                   | assert_statement
                                                   | empty_statement
                                                   | switch_statement
                                                   | do_statement
                                                   | break_statement
                                                   | continue_statement
                                                   | return_statement
                                                   | synchronized_statement
                                                   | throw_statement
                                                   | try_statement
                                                   | try_statement_with_resources'''
        p[0] = p[1]

    def p_expression_statement(self, p):
        '''expression_statement : statement_expression ';'
                                | explicit_constructor_invocation'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ExpressionStatement(p[1])

    def p_statement_expression(self, p):
        '''statement_expression : assignment
                                | pre_increment_expression
                                | pre_decrement_expression
                                | post_increment_expression
                                | post_decrement_expression
                                | method_invocation
                                | class_instance_creation_expression'''
        p[0] = p[1]

    def p_comma_opt(self, p):
        '''comma_opt : ','
                     | empty'''
        # ignore

    def p_array_initializer(self, p):
        '''array_initializer : '{' comma_opt '}' '''
        p[0] = ArrayInitializer()

    def p_array_initializer2(self, p):
        '''array_initializer : '{' variable_initializers '}'
                             | '{' variable_initializers ',' '}' '''
        p[0] = ArrayInitializer(p[2])

    def p_variable_initializers(self, p):
        '''variable_initializers : variable_initializer
                                 | variable_initializers ',' variable_initializer'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_method_invocation(self, p):
        '''method_invocation : NAME '(' argument_list_opt ')' '''
        p[0] = MethodInvocation(p[1], arguments=p[3])

    def p_method_invocation2(self, p):
        '''method_invocation : name '.' type_arguments NAME '(' argument_list_opt ')'
                             | primary '.' type_arguments NAME '(' argument_list_opt ')'
                             | SUPER '.' type_arguments NAME '(' argument_list_opt ')' '''
        p[0] = MethodInvocation(p[4], target=p[1], type_arguments=p[3], arguments=p[6])

    def p_method_invocation3(self, p):
        '''method_invocation : name '.' NAME '(' argument_list_opt ')'
                             | primary '.' NAME '(' argument_list_opt ')'
                             | SUPER '.' NAME '(' argument_list_opt ')' '''
        p[0] = MethodInvocation(p[3], target=p[1], arguments=p[5])

    def p_labeled_statement(self, p):
        '''labeled_statement : label ':' statement'''
        p[3].label = p[1]
        p[0] = p[3]

    def p_labeled_statement_no_short_if(self, p):
        '''labeled_statement_no_short_if : label ':' statement_no_short_if'''
        p[3].label = p[1]
        p[0] = p[3]

    def p_label(self, p):
        '''label : NAME'''
        p[0] = p[1]

    def p_if_then_statement(self, p):
        '''if_then_statement : IF '(' expression ')' statement'''
        p[0] = IfThenElse(p[3], p[5])

    def p_if_then_else_statement(self, p):
        '''if_then_else_statement : IF '(' expression ')' statement_no_short_if ELSE statement'''
        p[0] = IfThenElse(p[3], p[5], p[7])

    def p_if_then_else_statement_no_short_if(self, p):
        '''if_then_else_statement_no_short_if : IF '(' expression ')' statement_no_short_if ELSE statement_no_short_if'''
        p[0] = IfThenElse(p[3], p[5], p[7])

    def p_while_statement(self, p):
        '''while_statement : WHILE '(' expression ')' statement'''
        p[0] = While(p[3], p[5])

    def p_while_statement_no_short_if(self, p):
        '''while_statement_no_short_if : WHILE '(' expression ')' statement_no_short_if'''
        p[0] = While(p[3], p[5])

    def p_for_statement(self, p):
        '''for_statement : FOR '(' for_init_opt ';' expression_opt ';' for_update_opt ')' statement'''
        p[0] = For(p[3], p[5], p[7], p[9])

    def p_for_statement_no_short_if(self, p):
        '''for_statement_no_short_if : FOR '(' for_init_opt ';' expression_opt ';' for_update_opt ')' statement_no_short_if'''
        p[0] = For(p[3], p[5], p[7], p[9])

    def p_for_init_opt(self, p):
        '''for_init_opt : for_init
                        | empty'''
        p[0] = p[1]

    def p_for_init(self, p):
        '''for_init : statement_expression_list
                    | local_variable_declaration'''
        p[0] = p[1]

    def p_statement_expression_list(self, p):
        '''statement_expression_list : statement_expression
                                     | statement_expression_list ',' statement_expression'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_expression_opt(self, p):
        '''expression_opt : expression
                          | empty'''
        p[0] = p[1]

    def p_for_update_opt(self, p):
        '''for_update_opt : for_update
                          | empty'''
        p[0] = p[1]

    def p_for_update(self, p):
        '''for_update : statement_expression_list'''
        p[0] = p[1]

    def p_enhanced_for_statement(self, p):
        '''enhanced_for_statement : enhanced_for_statement_header statement'''
        p[0] = ForEach(p[1]['type'], p[1]['variable'], p[1]['iterable'], p[2], modifiers=p[1]['modifiers'])

    def p_enhanced_for_statement_no_short_if(self, p):
        '''enhanced_for_statement_no_short_if : enhanced_for_statement_header statement_no_short_if'''
        p[0] = ForEach(p[1]['type'], p[1]['variable'], p[1]['iterable'], p[2], modifiers=p[1]['modifiers'])

    def p_enhanced_for_statement_header(self, p):
        '''enhanced_for_statement_header : enhanced_for_statement_header_init ':' expression ')' '''
        p[1]['iterable'] = p[3]
        p[0] = p[1]

    def p_enhanced_for_statement_header_init(self, p):
        '''enhanced_for_statement_header_init : FOR '(' type NAME dims_opt'''
        p[0] = {'modifiers': [], 'type': p[3], 'variable': Variable(p[4], dimensions=p[5])}

    def p_enhanced_for_statement_header_init2(self, p):
        '''enhanced_for_statement_header_init : FOR '(' modifiers type NAME dims_opt'''
        p[0] = {'modifiers': p[3], 'type': p[4], 'variable': Variable(p[5], dimensions=p[6])}

    def p_statement_no_short_if(self, p):
        '''statement_no_short_if : statement_without_trailing_substatement
                                 | labeled_statement_no_short_if
                                 | if_then_else_statement_no_short_if
                                 | while_statement_no_short_if
                                 | for_statement_no_short_if
                                 | enhanced_for_statement_no_short_if'''
        p[0] = p[1]

    def p_assert_statement(self, p):
        '''assert_statement : ASSERT expression ';'
                            | ASSERT expression ':' expression ';' '''
        if len(p) == 4:
            p[0] = Assert(p[2])
        else:
            p[0] = Assert(p[2], message=p[4])

    def p_empty_statement(self, p):
        '''empty_statement : ';' '''
        p[0] = Empty()

    def p_switch_statement(self, p):
        '''switch_statement : SWITCH '(' expression ')' switch_block'''
        p[0] = Switch(p[3], p[5])

    def p_switch_block(self, p):
        '''switch_block : '{' '}' '''
        p[0] = []

    def p_switch_block2(self, p):
        '''switch_block : '{' switch_block_statements '}' '''
        p[0] = p[2]

    def p_switch_block3(self, p):
        '''switch_block : '{' switch_labels '}' '''
        p[0] = [SwitchCase(p[2])]

    def p_switch_block4(self, p):
        '''switch_block : '{' switch_block_statements switch_labels '}' '''
        p[0] = p[2] + [SwitchCase(p[3])]

    def p_switch_block_statements(self, p):
        '''switch_block_statements : switch_block_statement
                                   | switch_block_statements switch_block_statement'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_switch_block_statement(self, p):
        '''switch_block_statement : switch_labels block_statements'''
        p[0] = SwitchCase(p[1], body=p[2])

    def p_switch_labels(self, p):
        '''switch_labels : switch_label
                         | switch_labels switch_label'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_switch_label(self, p):
        '''switch_label : CASE constant_expression ':'
                        | DEFAULT ':' '''
        if len(p) == 3:
            p[0] = 'default'
        else:
            p[0] = p[2]

    def p_constant_expression(self, p):
        '''constant_expression : expression'''
        p[0] = p[1]

    def p_do_statement(self, p):
        '''do_statement : DO statement WHILE '(' expression ')' ';' '''
        p[0] = DoWhile(p[5], body=p[2])

    def p_break_statement(self, p):
        '''break_statement : BREAK ';'
                           | BREAK NAME ';' '''
        if len(p) == 3:
            p[0] = Break()
        else:
            p[0] = Break(p[2])

    def p_continue_statement(self, p):
        '''continue_statement : CONTINUE ';'
                              | CONTINUE NAME ';' '''
        if len(p) == 3:
            p[0] = Continue()
        else:
            p[0] = Continue(p[2])

    def p_return_statement(self, p):
        '''return_statement : RETURN expression_opt ';' '''
        p[0] = Return(p[2])

    def p_synchronized_statement(self, p):
        '''synchronized_statement : SYNCHRONIZED '(' expression ')' block'''
        p[0] = Synchronized(p[3], p[5])

    def p_throw_statement(self, p):
        '''throw_statement : THROW expression ';' '''
        p[0] = Throw(p[2])

    def p_try_statement(self, p):
        '''try_statement : TRY try_block catches
                         | TRY try_block catches_opt finally'''
        if len(p) == 4:
            p[0] = Try(p[2], catches=p[3])
        else:
            p[0] = Try(p[2], catches=p[3], _finally=p[4])

    def p_try_block(self, p):
        '''try_block : block'''
        p[0] = p[1]

    def p_catches(self, p):
        '''catches : catch_clause
                   | catches catch_clause'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_catches_opt(self, p):
        '''catches_opt : catches'''
        p[0] = p[1]

    def p_catches_opt2(self, p):
        '''catches_opt : empty'''
        p[0] = []

    def p_catch_clause(self, p):
        '''catch_clause : CATCH '(' catch_formal_parameter ')' block'''
        p[0] = Catch(p[3]['variable'], types=p[3]['types'], modifiers=p[3]['modifiers'], block=p[5])

    def p_catch_formal_parameter(self, p):
        '''catch_formal_parameter : modifiers_opt catch_type variable_declarator_id'''
        p[0] = {'modifiers': p[1], 'types': p[2], 'variable': p[3]}

    def p_catch_type(self, p):
        '''catch_type : union_type'''
        p[0] = p[1]

    def p_union_type(self, p):
        '''union_type : type
                      | union_type '|' type'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_try_statement_with_resources(self, p):
        '''try_statement_with_resources : TRY resource_specification try_block catches_opt
                                        | TRY resource_specification try_block catches_opt finally'''
        if len(p) == 5:
            p[0] = Try(p[3], resources=p[2], catches=p[4])
        else:
            p[0] = Try(p[3], resources=p[2], catches=p[4], _finally=p[5])

    def p_resource_specification(self, p):
        '''resource_specification : '(' resources semi_opt ')' '''
        p[0] = p[2]

    def p_semi_opt(self, p):
        '''semi_opt : ';'
                    | empty'''
        # ignore

    def p_resources(self, p):
        '''resources : resource
                     | resources trailing_semicolon resource'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_trailing_semicolon(self, p):
        '''trailing_semicolon : ';' '''
        # ignore

    def p_resource(self, p):
        '''resource : type variable_declarator_id '=' variable_initializer'''
        p[0] = Resource(p[2], type=p[1], initializer=p[4])

    def p_resource2(self, p):
        '''resource : modifiers type variable_declarator_id '=' variable_initializer'''
        p[0] = Resource(p[3], type=p[2], modifiers=p[1], initializer=p[5])

    def p_finally(self, p):
        '''finally : FINALLY block'''
        p[0] = p[2]

    def p_explicit_constructor_invocation(self, p):
        '''explicit_constructor_invocation : THIS '(' argument_list_opt ')' ';'
                                           | SUPER '(' argument_list_opt ')' ';' '''
        p[0] = ConstructorInvocation(p[1], arguments=p[3])

    def p_explicit_constructor_invocation2(self, p):
        '''explicit_constructor_invocation : type_arguments SUPER '(' argument_list_opt ')' ';'
                                           | type_arguments THIS '(' argument_list_opt ')' ';' '''
        p[0] = ConstructorInvocation(p[2], type_arguments=p[1], arguments=p[4])

    def p_explicit_constructor_invocation3(self, p):
        '''explicit_constructor_invocation : primary '.' SUPER '(' argument_list_opt ')' ';'
                                           | name '.' SUPER '(' argument_list_opt ')' ';'
                                           | primary '.' THIS '(' argument_list_opt ')' ';'
                                           | name '.' THIS '(' argument_list_opt ')' ';' '''
        p[0] = ConstructorInvocation(p[3], target=p[1], arguments=p[5])

    def p_explicit_constructor_invocation4(self, p):
        '''explicit_constructor_invocation : primary '.' type_arguments SUPER '(' argument_list_opt ')' ';'
                                           | name '.' type_arguments SUPER '(' argument_list_opt ')' ';'
                                           | primary '.' type_arguments THIS '(' argument_list_opt ')' ';'
                                           | name '.' type_arguments THIS '(' argument_list_opt ')' ';' '''
        p[0] = ConstructorInvocation(p[4], target=p[1], type_arguments=p[3], arguments=p[6])

    def p_class_instance_creation_expression(self, p):
        '''class_instance_creation_expression : NEW type_arguments class_type '(' argument_list_opt ')' class_body_opt'''
        p[0] = InstanceCreation(p[3], type_arguments=p[3], arguments=p[5], body=p[7])

    def p_class_instance_creation_expression2(self, p):
        '''class_instance_creation_expression : NEW class_type '(' argument_list_opt ')' class_body_opt'''
        p[0] = InstanceCreation(p[2], arguments=p[4], body=p[6])

    def p_class_instance_creation_expression3(self, p):
        '''class_instance_creation_expression : primary '.' NEW type_arguments class_type '(' argument_list_opt ')' class_body_opt'''
        p[0] = InstanceCreation(p[5], enclosed_in=p[1], type_arguments=p[4], arguments=p[7], body=p[9])

    def p_class_instance_creation_expression4(self, p):
        '''class_instance_creation_expression : primary '.' NEW class_type '(' argument_list_opt ')' class_body_opt'''
        p[0] = InstanceCreation(p[4], enclosed_in=p[1], arguments=p[6], body=p[8])

    def p_class_instance_creation_expression5(self, p):
        '''class_instance_creation_expression : class_instance_creation_expression_name NEW class_type '(' argument_list_opt ')' class_body_opt'''
        p[0] = InstanceCreation(p[3], enclosed_in=p[1], arguments=p[5], body=p[7])

    def p_class_instance_creation_expression6(self, p):
        '''class_instance_creation_expression : class_instance_creation_expression_name NEW type_arguments class_type '(' argument_list_opt ')' class_body_opt'''
        p[0] = InstanceCreation(p[4], enclosed_in=p[1], type_arguments=p[3], arguments=p[6], body=p[8])

    def p_class_instance_creation_expression_name(self, p):
        '''class_instance_creation_expression_name : name '.' '''
        p[0] = p[1]

    def p_class_body_opt(self, p):
        '''class_body_opt : class_body
                          | empty'''
        p[0] = p[1]

    def p_field_access(self, p):
        '''field_access : primary '.' NAME
                        | SUPER '.' NAME'''
        p[0] = FieldAccess(p[3], p[1])

    def p_array_access(self, p):
        '''array_access : name '[' expression ']'
                        | primary_no_new_array '[' expression ']'
                        | array_creation_with_array_initializer '[' expression ']' '''
        p[0] = ArrayAccess(p[3], p[1])

    def p_array_creation_with_array_initializer(self, p):
        '''array_creation_with_array_initializer : NEW primitive_type dim_with_or_without_exprs array_initializer
                                                 | NEW class_or_interface_type dim_with_or_without_exprs array_initializer'''
        p[0] = ArrayCreation(p[2], dimensions=p[3], initializer=p[4])

    def p_dim_with_or_without_exprs(self, p):
        '''dim_with_or_without_exprs : dim_with_or_without_expr
                                     | dim_with_or_without_exprs dim_with_or_without_expr'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_dim_with_or_without_expr(self, p):
        '''dim_with_or_without_expr : '[' expression ']'
                                    | '[' ']' '''
        if len(p) == 3:
            p[0] = None
        else:
            p[0] = p[2]

    def p_array_creation_without_array_initializer(self, p):
        '''array_creation_without_array_initializer : NEW primitive_type dim_with_or_without_exprs
                                                    | NEW class_or_interface_type dim_with_or_without_exprs'''
        p[0] = ArrayCreation(p[2], dimensions=p[3])

class NameParser(object):

    def p_name(self, p):
        '''name : simple_name
                | qualified_name'''
        p[0] = p[1]

    def p_simple_name(self, p):
        '''simple_name : NAME'''
        p[0] = Name(p[1])

    def p_qualified_name(self, p):
        '''qualified_name : name '.' simple_name'''
        p[1].append_name(p[3])
        p[0] = p[1]

class LiteralParser(object):

    def p_literal(self, p):
        '''literal : NUM
                   | CHAR_LITERAL
                   | STRING_LITERAL
                   | TRUE
                   | FALSE
                   | NULL'''
        p[0] = Literal(p[1])

class TypeParser(object):

    def p_modifiers_opt(self, p):
        '''modifiers_opt : modifiers'''
        p[0] = p[1]

    def p_modifiers_opt2(self, p):
        '''modifiers_opt : empty'''
        p[0] = []

    def p_modifiers(self, p):
        '''modifiers : modifier
                     | modifiers modifier'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_modifier(self, p):
        '''modifier : PUBLIC
                    | PROTECTED
                    | PRIVATE
                    | STATIC
                    | ABSTRACT
                    | FINAL
                    | NATIVE
                    | SYNCHRONIZED
                    | TRANSIENT
                    | VOLATILE
                    | STRICTFP
                    | annotation'''
        p[0] = p[1]

    def p_type(self, p):
        '''type : primitive_type
                | reference_type'''
        p[0] = p[1]

    def p_primitive_type(self, p):
        '''primitive_type : BOOLEAN
                          | VOID
                          | BYTE
                          | SHORT
                          | INT
                          | LONG
                          | CHAR
                          | FLOAT
                          | DOUBLE'''
        p[0] = p[1]

    def p_reference_type(self, p):
        '''reference_type : class_or_interface_type
                          | array_type'''
        p[0] = p[1]

    def p_class_or_interface_type(self, p):
        '''class_or_interface_type : class_or_interface
                                   | generic_type'''
        p[0] = p[1]

    def p_class_type(self, p):
        '''class_type : class_or_interface_type'''
        p[0] = p[1]

    def p_class_or_interface(self, p):
        '''class_or_interface : name
                              | generic_type '.' name'''
        if len(p) == 2:
            p[0] = Type(p[1])
        else:
            p[0] = Type(p[3], enclosed_in=p[1])

    def p_generic_type(self, p):
        '''generic_type : class_or_interface type_arguments'''
        p[1].type_arguments = p[2]
        p[0] = p[1]

    def p_generic_type2(self, p):
        '''generic_type : class_or_interface '<' '>' '''
        p[0] = Type(p[1], type_arguments='diamond')

#    def p_array_type(self, p):
#        '''array_type : primitive_type dims
#                      | name dims
#                      | array_type_with_type_arguments_name dims
#                      | generic_type dims'''
#        p[0] = p[1] + '[' + p[2] + ']'
#
#    def p_array_type_with_type_arguments_name(self, p):
#        '''array_type_with_type_arguments_name : generic_type '.' name'''
#        p[0] = p[1] + '.' + p[3]

    def p_array_type(self, p):
        '''array_type : primitive_type dims
                      | name dims'''
        p[0] = Type(p[1], dimensions=p[2])

    def p_array_type2(self, p):
        '''array_type : generic_type dims'''
        p[1].dims = p[2]
        p[0] = p[1]

    def p_array_type3(self, p):
        '''array_type : generic_type '.' name dims'''
        p[0] = Type(p[3], enclosed_in=p[1], dimensions=p[4])

    def p_type_arguments(self, p):
        '''type_arguments : '<' type_argument_list1'''
        p[0] = p[2]

    def p_type_argument_list1(self, p):
        '''type_argument_list1 : type_argument1
                               | type_argument_list ',' type_argument1'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_type_argument_list(self, p):
        '''type_argument_list : type_argument
                              | type_argument_list ',' type_argument'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_type_argument(self, p):
        '''type_argument : reference_type
                         | wildcard'''
        p[0] = p[1]

    def p_type_argument1(self, p):
        '''type_argument1 : reference_type1
                          | wildcard1'''
        p[0] = p[1]

    def p_reference_type1(self, p):
        '''reference_type1 : reference_type '>'
                           | class_or_interface '<' type_argument_list2'''
        if len(p) == 3:
            p[0] = p[1]
        else:
            p[1].type_arguments = p[3]
            p[0] = p[1]

    def p_type_argument_list2(self, p):
        '''type_argument_list2 : type_argument2
                               | type_argument_list ',' type_argument2'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_type_argument2(self, p):
        '''type_argument2 : reference_type2
                          | wildcard2'''
        p[0] = p[1]

    def p_reference_type2(self, p):
        '''reference_type2 : reference_type RSHIFT
                           | class_or_interface '<' type_argument_list3'''
        if len(p) == 3:
            p[0] = p[1]
        else:
            p[1].type_arguments = p[3]
            p[0] = p[1]

    def p_type_argument_list3(self, p):
        '''type_argument_list3 : type_argument3
                               | type_argument_list ',' type_argument3'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_type_argument3(self, p):
        '''type_argument3 : reference_type3
                          | wildcard3'''
        p[0] = p[1]

    def p_reference_type3(self, p):
        '''reference_type3 : reference_type RRSHIFT'''
        p[0] = p[1]

    def p_wildcard(self, p):
        '''wildcard : '?'
                    | '?' wildcard_bounds'''
        if len(p) == 2:
            p[0] = Wildcard()
        else:
            p[0] = Wildcard(bounds=p[2])

    def p_wildcard_bounds(self, p):
        '''wildcard_bounds : EXTENDS reference_type
                           | SUPER reference_type'''
        if p[1] == 'extends':
            p[0] = WildcardBound(p[2], extends=True)
        else:
            p[0] = WildcardBound(p[2], _super=True)

    def p_wildcard1(self, p):
        '''wildcard1 : '?' '>'
                     | '?' wildcard_bounds1'''
        if p[2] == '>':
            p[0] = Wildcard()
        else:
            p[0] = Wildcard(bounds=p[2])

    def p_wildcard_bounds1(self, p):
        '''wildcard_bounds1 : EXTENDS reference_type1
                            | SUPER reference_type1'''
        if p[1] == 'extends':
            p[0] = WildcardBound(p[2], extends=True)
        else:
            p[0] = WildcardBound(p[2], _super=True)

    def p_wildcard2(self, p):
        '''wildcard2 : '?' RSHIFT
                     | '?' wildcard_bounds2'''
        if p[2] == '>>':
            p[0] = Wildcard()
        else:
            p[0] = Wildcard(bounds=p[2])

    def p_wildcard_bounds2(self, p):
        '''wildcard_bounds2 : EXTENDS reference_type2
                            | SUPER reference_type2'''
        if p[1] == 'extends':
            p[0] = WildcardBound(p[2], extends=True)
        else:
            p[0] = WildcardBound(p[2], _super=True)

    def p_wildcard3(self, p):
        '''wildcard3 : '?' RRSHIFT
                     | '?' wildcard_bounds3'''
        if p[2] == '>>>':
            p[0] = Wildcard()
        else:
            p[0] = Wildcard(bounds=p[2])

    def p_wildcard_bounds3(self, p):
        '''wildcard_bounds3 : EXTENDS reference_type3
                            | SUPER reference_type3'''
        if p[1] == 'extends':
            p[0] = WildcardBound(p[2], extends=True)
        else:
            p[0] = WildcardBound(p[2], _super=True)

    def p_type_parameter_header(self, p):
        '''type_parameter_header : NAME'''
        p[0] = p[1]

    def p_type_parameters(self, p):
        '''type_parameters : '<' type_parameter_list1'''
        p[0] = p[2]

    def p_type_parameter_list(self, p):
        '''type_parameter_list : type_parameter
                               | type_parameter_list ',' type_parameter'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_type_parameter(self, p):
        '''type_parameter : type_parameter_header
                          | type_parameter_header EXTENDS reference_type
                          | type_parameter_header EXTENDS reference_type additional_bound_list'''
        if len(p) == 2:
            p[0] = TypeParameter(p[1])
        elif len(p) == 4:
            p[0] = TypeParameter(p[1], extends=[p[3]])
        else:
            p[0] = TypeParameter(p[1], extends=[p[3]] + p[4])

    def p_additional_bound_list(self, p):
        '''additional_bound_list : additional_bound
                                 | additional_bound_list additional_bound'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_additional_bound(self, p):
        '''additional_bound : '&' reference_type'''
        p[0] = p[2]

    def p_type_parameter_list1(self, p):
        '''type_parameter_list1 : type_parameter1
                                | type_parameter_list ',' type_parameter1'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_type_parameter1(self, p):
        '''type_parameter1 : type_parameter_header '>'
                           | type_parameter_header EXTENDS reference_type1
                           | type_parameter_header EXTENDS reference_type additional_bound_list1'''
        if len(p) == 3:
            p[0] = TypeParameter(p[1])
        elif len(p) == 4:
            p[0] = TypeParameter(p[1], extends=[p[3]])
        else:
            p[0] = TypeParameter(p[1], extends=[p[3]] + p[4])

    def p_additional_bound_list1(self, p):
        '''additional_bound_list1 : additional_bound1
                                  | additional_bound_list additional_bound1'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_additional_bound1(self, p):
        '''additional_bound1 : '&' reference_type1'''
        p[0] = p[2]

class ClassParser(object):

    def p_type_declaration(self, p):
        '''type_declaration : class_declaration
                            | interface_declaration
                            | enum_declaration
                            | annotation_type_declaration'''
        p[0] = p[1]

    def p_type_declaration2(self, p):
        '''type_declaration : ';' '''
        p[0] = EmptyDeclaration()

    def p_class_declaration(self, p):
        '''class_declaration : class_header class_body'''
        p[0] = ClassDeclaration(p[1]['name'], p[2], modifiers=p[1]['modifiers'],
                                extends=p[1]['extends'], implements=p[1]['implements'],
                                type_parameters=p[1]['type_parameters'])

    def p_class_header(self, p):
        '''class_header : class_header_name class_header_extends_opt class_header_implements_opt'''
        p[1]['extends'] = p[2]
        p[1]['implements'] = p[3]
        p[0] = p[1]

    def p_class_header_name(self, p):
        '''class_header_name : class_header_name1 type_parameters
                             | class_header_name1'''
        if len(p) == 2:
            p[1]['type_parameters'] = []
        else:
            p[1]['type_parameters'] = p[2]
        p[0] = p[1]

    def p_class_header_name1(self, p):
        '''class_header_name1 : modifiers_opt CLASS NAME'''
        p[0] = {'modifiers': p[1], 'name': p[3]}

    def p_class_header_extends_opt(self, p):
        '''class_header_extends_opt : class_header_extends
                                    | empty'''
        p[0] = p[1]

    def p_class_header_extends(self, p):
        '''class_header_extends : EXTENDS class_type'''
        p[0] = p[2]

    def p_class_header_implements_opt(self, p):
        '''class_header_implements_opt : class_header_implements
                                       | empty'''
        p[0] = p[1]

    def p_class_header_implements(self, p):
        '''class_header_implements : IMPLEMENTS interface_type_list'''
        p[0] = p[2]

    def p_interface_type_list(self, p):
        '''interface_type_list : interface_type
                               | interface_type_list ',' interface_type'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_interface_type(self, p):
        '''interface_type : class_or_interface_type'''
        p[0] = p[1]

    def p_class_body(self, p):
        '''class_body : '{' class_body_declarations_opt '}' '''
        p[0] = p[2]

    def p_class_body_declarations_opt(self, p):
        '''class_body_declarations_opt : class_body_declarations'''
        p[0] = p[1]

    def p_class_body_declarations_opt2(self, p):
        '''class_body_declarations_opt : empty'''
        p[0] = []

    def p_class_body_declarations(self, p):
        '''class_body_declarations : class_body_declaration
                                   | class_body_declarations class_body_declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_class_body_declaration(self, p):
        '''class_body_declaration : class_member_declaration
                                  | static_initializer
                                  | constructor_declaration'''
        p[0] = p[1]

    def p_class_body_declaration2(self, p):
        '''class_body_declaration : block'''
        p[0] = ClassInitializer(p[1])

    def p_class_member_declaration(self, p):
        '''class_member_declaration : field_declaration
                                    | class_declaration
                                    | method_declaration
                                    | interface_declaration
                                    | enum_declaration
                                    | annotation_type_declaration'''
        p[0] = p[1]

    def p_class_member_declaration2(self, p):
        '''class_member_declaration : ';' '''
        p[0] = EmptyDeclaration()

    def p_field_declaration(self, p):
        '''field_declaration : modifiers_opt type variable_declarators ';' '''
        p[0] = FieldDeclaration(p[2], p[3], modifiers=p[1])

    def p_static_initializer(self, p):
        '''static_initializer : STATIC block'''
        p[0] = ClassInitializer(p[2], static=True)

    def p_constructor_declaration(self, p):
        '''constructor_declaration : constructor_header method_body'''
        p[0] = ConstructorDeclaration(p[1]['name'], p[2], modifiers=p[1]['modifiers'],
                                      type_parameters=p[1]['type_parameters'],
                                      parameters=p[1]['parameters'], throws=p[1]['throws'])

    def p_constructor_header(self, p):
        '''constructor_header : constructor_header_name formal_parameter_list_opt ')' method_header_throws_clause_opt'''
        p[1]['parameters'] = p[2]
        p[1]['throws'] = p[4]
        p[0] = p[1]

    def p_constructor_header_name(self, p):
        '''constructor_header_name : modifiers_opt type_parameters NAME '('
                                   | modifiers_opt NAME '(' '''
        if len(p) == 4:
            p[0] = {'modifiers': p[1], 'type_parameters': [], 'name': p[2]}
        else:
            p[0] = {'modifiers': p[1], 'type_parameters': p[2], 'name': p[3]}

    def p_formal_parameter_list_opt(self, p):
        '''formal_parameter_list_opt : formal_parameter_list'''
        p[0] = p[1]

    def p_formal_parameter_list_opt2(self, p):
        '''formal_parameter_list_opt : empty'''
        p[0] = []

    def p_formal_parameter_list(self, p):
        '''formal_parameter_list : formal_parameter
                                 | formal_parameter_list ',' formal_parameter'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_formal_parameter(self, p):
        '''formal_parameter : modifiers_opt type variable_declarator_id
                            | modifiers_opt type ELLIPSIS variable_declarator_id'''
        if len(p) == 4:
            p[0] = FormalParameter(p[3], p[2], modifiers=p[1])
        else:
            p[0] = FormalParameter(p[4], p[2], modifiers=p[1], vararg=True)

    def p_method_header_throws_clause_opt(self, p):
        '''method_header_throws_clause_opt : method_header_throws_clause
                                           | empty'''
        p[0] = p[1]

    def p_method_header_throws_clause(self, p):
        '''method_header_throws_clause : THROWS class_type_list'''
        p[0] = Throws(p[2])

    def p_class_type_list(self, p):
        '''class_type_list : class_type_elt
                           | class_type_list ',' class_type_elt'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_class_type_elt(self, p):
        '''class_type_elt : class_type'''
        p[0] = p[1]

    def p_method_body(self, p):
        '''method_body : '{' block_statements_opt '}' '''
        p[0] = p[2]

    def p_method_declaration(self, p):
        '''method_declaration : abstract_method_declaration
                              | method_header method_body'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = MethodDeclaration(p[1]['name'], parameters=p[1]['parameters'],
                                     extended_dims=p[1]['extended_dims'], type_parameters=p[1]['type_parameters'],
                                     return_type=p[1]['type'], modifiers=p[1]['modifiers'],
                                     throws=p[1]['throws'], body=p[2])

    def p_abstract_method_declaration(self, p):
        '''abstract_method_declaration : method_header ';' '''
        p[0] = MethodDeclaration(p[1]['name'], abstract=True, parameters=p[1]['parameters'],
                                 extended_dims=p[1]['extended_dims'], type_parameters=p[1]['type_parameters'],
                                 return_type=p[1]['type'], modifiers=p[1]['modifiers'],
                                 throws=p[1]['throws'])

    def p_method_header(self, p):
        '''method_header : method_header_name formal_parameter_list_opt ')' method_header_extended_dims method_header_throws_clause_opt'''
        p[1]['parameters'] = p[2]
        p[1]['extended_dims'] = p[4]
        p[1]['throws'] = p[5]
        p[0] = p[1]

    def p_method_header_name(self, p):
        '''method_header_name : modifiers_opt type_parameters type NAME '('
                              | modifiers_opt type NAME '(' '''
        if len(p) == 5:
            p[0] = {'modifiers': p[1], 'type_parameters': [], 'type': p[2], 'name': p[3]}
        else:
            p[0] = {'modifiers': p[1], 'type_parameters': p[2], 'type': p[3], 'name': p[4]}

    def p_method_header_extended_dims(self, p):
        '''method_header_extended_dims : dims_opt'''
        p[0] = p[1]

    def p_interface_declaration(self, p):
        '''interface_declaration : interface_header interface_body'''
        p[0] = InterfaceDeclaration(p[1]['name'], modifiers=p[1]['modifiers'],
                                    type_parameters=p[1]['type_parameters'],
                                    extends=p[1]['extends'],
                                    body=p[2])

    def p_interface_header(self, p):
        '''interface_header : interface_header_name interface_header_extends_opt'''
        p[1]['extends'] = p[2]
        p[0] = p[1]

    def p_interface_header_name(self, p):
        '''interface_header_name : interface_header_name1 type_parameters
                                 | interface_header_name1'''
        if len(p) == 2:
            p[1]['type_parameters'] = []
        else:
            p[1]['type_parameters'] = p[2]
        p[0] = p[1]

    def p_interface_header_name1(self, p):
        '''interface_header_name1 : modifiers_opt INTERFACE NAME'''
        p[0] = {'modifiers': p[1], 'name': p[3]}

    def p_interface_header_extends_opt(self, p):
        '''interface_header_extends_opt : interface_header_extends'''
        p[0] = p[1]

    def p_interface_header_extends_opt2(self, p):
        '''interface_header_extends_opt : empty'''
        p[0] = []

    def p_interface_header_extends(self, p):
        '''interface_header_extends : EXTENDS interface_type_list'''
        p[0] = p[2]

    def p_interface_body(self, p):
        '''interface_body : '{' interface_member_declarations_opt '}' '''
        p[0] = p[2]

    def p_interface_member_declarations_opt(self, p):
        '''interface_member_declarations_opt : interface_member_declarations'''
        p[0] = p[1]

    def p_interface_member_declarations_opt2(self, p):
        '''interface_member_declarations_opt : empty'''
        p[0] = []

    def p_interface_member_declarations(self, p):
        '''interface_member_declarations : interface_member_declaration
                                         | interface_member_declarations interface_member_declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_interface_member_declaration(self, p):
        '''interface_member_declaration : constant_declaration
                                        | abstract_method_declaration
                                        | class_declaration
                                        | interface_declaration
                                        | enum_declaration
                                        | annotation_type_declaration'''
        p[0] = p[1]

    def p_interface_member_declaration2(self, p):
        '''interface_member_declaration : ';' '''
        p[0] = EmptyDeclaration()

    def p_constant_declaration(self, p):
        '''constant_declaration : field_declaration'''
        p[0] = p[1]

    def p_enum_declaration(self, p):
        '''enum_declaration : enum_header enum_body'''
        p[0] = EnumDeclaration(p[1]['name'], implements=p[1]['implements'],
                               modifiers=p[1]['modifiers'],
                               type_parameters=p[1]['type_parameters'], body=p[2])

    def p_enum_header(self, p):
        '''enum_header : enum_header_name class_header_implements_opt'''
        p[1]['implements'] = p[2]
        p[0] = p[1]

    def p_enum_header_name(self, p):
        '''enum_header_name : modifiers_opt ENUM NAME
                            | modifiers_opt ENUM NAME type_parameters'''
        if len(p) == 4:
            p[0] = {'modifiers': p[1], 'name': p[3], 'type_parameters': []}
        else:
            p[0] = {'modifiers': p[1], 'name': p[3], 'type_parameters': p[4]}

    def p_enum_body(self, p):
        '''enum_body : '{' enum_body_declarations_opt '}' '''
        p[0] = p[2]

    def p_enum_body2(self, p):
        '''enum_body : '{' ',' enum_body_declarations_opt '}' '''
        p[0] = p[3]

    def p_enum_body3(self, p):
        '''enum_body : '{' enum_constants ',' enum_body_declarations_opt '}' '''
        p[0] = p[2] + p[4]

    def p_enum_body4(self, p):
        '''enum_body : '{' enum_constants enum_body_declarations_opt '}' '''
        p[0] = p[2] + p[3]

    def p_enum_constants(self, p):
        '''enum_constants : enum_constant
                          | enum_constants ',' enum_constant'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_enum_constant(self, p):
        '''enum_constant : enum_constant_header class_body
                         | enum_constant_header'''
        if len(p) == 2:
            p[0] = EnumConstant(p[1]['name'], arguments=p[1]['arguments'], modifiers=p[1]['modifiers'])
        else:
            p[0] = EnumConstant(p[1]['name'], arguments=p[1]['arguments'], modifiers=p[1]['modifiers'], body=p[2])

    def p_enum_constant_header(self, p):
        '''enum_constant_header : enum_constant_header_name arguments_opt'''
        p[1]['arguments'] = p[2]
        p[0] = p[1]

    def p_enum_constant_header_name(self, p):
        '''enum_constant_header_name : modifiers_opt NAME'''
        p[0] = {'modifiers': p[1], 'name': p[2]}

    def p_arguments_opt(self, p):
        '''arguments_opt : arguments'''
        p[0] = p[1]

    def p_arguments_opt2(self, p):
        '''arguments_opt : empty'''
        p[0] = []

    def p_arguments(self, p):
        '''arguments : '(' argument_list_opt ')' '''
        p[0] = p[2]

    def p_argument_list_opt(self, p):
        '''argument_list_opt : argument_list'''
        p[0] = p[1]

    def p_argument_list_opt2(self, p):
        '''argument_list_opt : empty'''
        p[0] = []

    def p_argument_list(self, p):
        '''argument_list : expression
                         | argument_list ',' expression'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_enum_body_declarations_opt(self, p):
        '''enum_body_declarations_opt : enum_declarations'''
        p[0] = p[1]

    def p_enum_body_declarations_opt2(self, p):
        '''enum_body_declarations_opt : empty'''
        p[0] = []

    def p_enum_body_declarations(self, p):
        '''enum_declarations : ';' class_body_declarations_opt'''
        p[0] = p[2]

    def p_annotation_type_declaration(self, p):
        '''annotation_type_declaration : annotation_type_declaration_header annotation_type_body'''
        p[0] = AnnotationDeclaration(p[1]['name'], modifiers=p[1]['modifiers'],
                              type_parameters=p[1]['type_parameters'],
                              extends=p[1]['extends'], implements=p[1]['implements'],
                              body=p[2])

    def p_annotation_type_declaration_header(self, p):
        '''annotation_type_declaration_header : annotation_type_declaration_header_name class_header_extends_opt class_header_implements_opt'''
        p[1]['extends'] = p[2]
        p[1]['implements'] = p[3]
        p[0] = p[1]

    def p_annotation_type_declaration_header_name(self, p):
        '''annotation_type_declaration_header_name : modifiers '@' INTERFACE NAME'''
        p[0] = {'modifiers': p[1], 'name': p[4], 'type_parameters': []}

    def p_annotation_type_declaration_header_name2(self, p):
        '''annotation_type_declaration_header_name : modifiers '@' INTERFACE NAME type_parameters'''
        p[0] = {'modifiers': p[1], 'name': p[4], 'type_parameters': p[5]}

    def p_annotation_type_declaration_header_name3(self, p):
        '''annotation_type_declaration_header_name : '@' INTERFACE NAME type_parameters'''
        p[0] = {'modifiers': [], 'name': p[3], 'type_parameters': p[4]}

    def p_annotation_type_declaration_header_name4(self, p):
        '''annotation_type_declaration_header_name : '@' INTERFACE NAME'''
        p[0] = {'modifiers': [], 'name': p[3], 'type_parameters': []}

    def p_annotation_type_body(self, p):
        '''annotation_type_body : '{' annotation_type_member_declarations_opt '}' '''
        p[0] = p[2]

    def p_annotation_type_member_declarations_opt(self, p):
        '''annotation_type_member_declarations_opt : annotation_type_member_declarations'''
        p[0] = p[1]

    def p_annotation_type_member_declarations_opt2(self, p):
        '''annotation_type_member_declarations_opt : empty'''
        p[0] = []

    def p_annotation_type_member_declarations(self, p):
        '''annotation_type_member_declarations : annotation_type_member_declaration
                                               | annotation_type_member_declarations annotation_type_member_declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_annotation_type_member_declaration(self, p):
        '''annotation_type_member_declaration : annotation_method_header ';'
                                              | constant_declaration
                                              | constructor_declaration
                                              | type_declaration'''
        p[0] = p[1]

    def p_annotation_method_header(self, p):
        '''annotation_method_header : annotation_method_header_name formal_parameter_list_opt ')' method_header_extended_dims annotation_method_header_default_value_opt'''
        p[0] = AnnotationMethodDeclaration(p[1]['name'], p[1]['type'], parameters=p[2],
                                           default=p[5], extended_dims=p[4],
                                           type_parameters=p[1]['type_parameters'],
                                           modifiers=p[1]['modifiers'])

    def p_annotation_method_header_name(self, p):
        '''annotation_method_header_name : modifiers_opt type_parameters type NAME '('
                                         | modifiers_opt type NAME '(' '''
        if len(p) == 5:
            p[0] = {'modifiers': p[1], 'type_parameters': [], 'type': p[2], 'name': p[3]}
        else:
            p[0] = {'modifiers': p[1], 'type_parameters': p[2], 'type': p[3], 'name': p[4]}

    def p_annotation_method_header_default_value_opt(self, p):
        '''annotation_method_header_default_value_opt : default_value
                                                      | empty'''
        p[0] = p[1]

    def p_default_value(self, p):
        '''default_value : DEFAULT member_value'''
        p[0] = p[2]

    def p_member_value(self, p):
        '''member_value : conditional_expression_not_name
                        | name
                        | annotation
                        | member_value_array_initializer'''
        p[0] = p[1]

    def p_member_value_array_initializer(self, p):
        '''member_value_array_initializer : '{' member_values ',' '}'
                                          | '{' member_values '}' '''
        p[0] = ArrayInitializer(p[2])

    def p_member_value_array_initializer2(self, p):
        '''member_value_array_initializer : '{' ',' '}'
                                          | '{' '}' '''
        # ignore

    def p_member_values(self, p):
        '''member_values : member_value
                         | member_values ',' member_value'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_annotation(self, p):
        '''annotation : normal_annotation
                      | marker_annotation
                      | single_member_annotation'''
        p[0] = p[1]

    def p_normal_annotation(self, p):
        '''normal_annotation : annotation_name '(' member_value_pairs_opt ')' '''
        p[0] = Annotation(p[1], members=p[3])

    def p_annotation_name(self, p):
        '''annotation_name : '@' name'''
        p[0] = p[2]

    def p_member_value_pairs_opt(self, p):
        '''member_value_pairs_opt : member_value_pairs'''
        p[0] = p[1]

    def p_member_value_pairs_opt2(self, p):
        '''member_value_pairs_opt : empty'''
        p[0] = []

    def p_member_value_pairs(self, p):
        '''member_value_pairs : member_value_pair
                              | member_value_pairs ',' member_value_pair'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_member_value_pair(self, p):
        '''member_value_pair : simple_name '=' member_value'''
        p[0] = AnnotationMember(p[1], p[3])

    def p_marker_annotation(self, p):
        '''marker_annotation : annotation_name'''
        p[0] = Annotation(p[1])

    def p_single_member_annotation(self, p):
        '''single_member_annotation : annotation_name '(' single_member_annotation_member_value ')' '''
        p[0] = Annotation(p[1], single_member=p[3])

    def p_single_member_annotation_member_value(self, p):
        '''single_member_annotation_member_value : member_value'''
        p[0] = p[1]

class CompilationUnitParser(object):

    def p_compilation_unit(self, p):
        '''compilation_unit : package_declaration'''
        p[0] = CompilationUnit(package_declaration=p[1])

    def p_compilation_unit2(self, p):
        '''compilation_unit : package_declaration import_declarations'''
        p[0] = CompilationUnit(package_declaration=p[1], import_declarations=p[2])

    def p_compilation_unit3(self, p):
        '''compilation_unit : package_declaration import_declarations type_declarations'''
        p[0] = CompilationUnit(package_declaration=p[1], import_declarations=p[2], type_declarations=p[3])

    def p_compilation_unit4(self, p):
        '''compilation_unit : package_declaration type_declarations'''
        p[0] = CompilationUnit(package_declaration=p[1], type_declarations=p[2])

    def p_compilation_unit5(self, p):
        '''compilation_unit : import_declarations'''
        p[0] = CompilationUnit(import_declarations=p[1])

    def p_compilation_unit6(self, p):
        '''compilation_unit : type_declarations'''
        p[0] = CompilationUnit(type_declarations=p[1])

    def p_compilation_unit7(self, p):
        '''compilation_unit : import_declarations type_declarations'''
        p[0] = CompilationUnit(import_declarations=p[1], type_declarations=p[2])

    def p_compilation_unit8(self, p):
        '''compilation_unit : empty'''
        p[0] = CompilationUnit()

    def p_package_declaration(self, p):
        '''package_declaration : package_declaration_name ';' '''
        if p[1][0]:
            p[0] = PackageDeclaration(p[1][1], modifiers=p[1][0])
        else:
            p[0] = PackageDeclaration(p[1][1])

    def p_package_declaration_name(self, p):
        '''package_declaration_name : modifiers PACKAGE name
                                    | PACKAGE name'''
        if len(p) == 3:
            p[0] = (None, p[2])
        else:
            p[0] = (p[1], p[3])

    def p_import_declarations(self, p):
        '''import_declarations : import_declaration
                               | import_declarations import_declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_import_declaration(self, p):
        '''import_declaration : single_type_import_declaration
                              | type_import_on_demand_declaration
                              | single_static_import_declaration
                              | static_import_on_demand_declaration'''
        p[0] = p[1]

    def p_single_type_import_declaration(self, p):
        '''single_type_import_declaration : IMPORT name ';' '''
        p[0] = ImportDeclaration(p[2])

    def p_type_import_on_demand_declaration(self, p):
        '''type_import_on_demand_declaration : IMPORT name '.' '*' ';' '''
        p[0] = ImportDeclaration(p[2], on_demand=True)

    def p_single_static_import_declaration(self, p):
        '''single_static_import_declaration : IMPORT STATIC name ';' '''
        p[0] = ImportDeclaration(p[3], static=True)

    def p_static_import_on_demand_declaration(self, p):
        '''static_import_on_demand_declaration : IMPORT STATIC name '.' '*' ';' '''
        p[0] = ImportDeclaration(p[3], static=True, on_demand=True)

    def p_type_declarations(self, p):
        '''type_declarations : type_declaration
                             | type_declarations type_declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

class MyParser(ExpressionParser, NameParser, LiteralParser, TypeParser, ClassParser, StatementParser, CompilationUnitParser):

    tokens = MyLexer.tokens

    def p_goal_compilation_unit(self, p):
        '''goal : PLUSPLUS compilation_unit'''
        p[0] = p[2]

    def p_goal_expression(self, p):
        '''goal : MINUSMINUS expression'''
        p[0] = p[2]

    def p_goal_statement(self, p):
        '''goal : '*' block_statement'''
        p[0] = p[2]

    def p_error(self, p):
        common.logger.debug('error: {}'.format(p))

    def p_empty(self, p):
        '''empty :'''

class Parser(object):

    def __init__(self):
        self.lexer = lex.lex(module=MyLexer(), optimize=1)
        self.parser = yacc.yacc(module=MyParser(), start='goal', optimize=1)

    def tokenize_string(self, code):
        self.lexer.input(code)
        for token in self.lexer:
            print(token)

    def tokenize_file(self, _file):
        if type(_file) == str:
            _file = open(_file)
        content = ''
        for line in _file:
            content += line
        return self.tokenize_string(content)

    def parse_expression(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='--')

    def parse_statement(self, code, debug=0, lineno=1):
        return self.parse_string(code, debug, lineno, prefix='* ')

    def parse_string(self, code, debug=0, lineno=1, prefix='++'):
      	self.lexer.lineno = lineno
        return self.parser.parse(prefix + code, lexer=self.lexer, debug=debug)


    def parse_file(self, _file, debug=0):
        if type(_file) == str:
            _file = open(_file)
        content = _file.read()
        return self.parse_string(content,debug=debug)

if __name__ == '__main__':
    # for testing
    lexer = lex.lex(module=MyLexer())
    parser = yacc.yacc(module=MyParser(), write_tables=0, start='type_parameters')

    expressions = [
        '<T extends Foo & Bar>'
    ]

    for expr in expressions:
        print('lexing expression {}'.format(expr))
        lexer.input(expr)
        for token in lexer:
            print(token)

        print('parsing expression {}'.format(expr))
        t = parser.parse(expr, lexer=lexer, debug=1)
        print('result: {}'.format(t))
        print('--------------------------------')

