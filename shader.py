from OpenGL.GL import *

class ShaderProgram:

    def __init__(self, vertex_source = None, fragment_source = None) -> None:
        if vertex_source is not None:
            self.vertex_shader = self._compile_program(vertex_source, GL_VERTEX_SHADER)
        
        if fragment_source is not None:
            self.fragment_shader = self._compile_program(fragment_source, GL_FRAGMENT_SHADER)
        
        self.shader_program = glCreateProgram()

        glAttachShader(self.shader_program, self.vertex_shader)
        glAttachShader(self.shader_program, self.fragment_shader)

        glLinkProgram(self.shader_program)

        success = glGetProgramiv(self.shader_program, GL_LINK_STATUS)

        if success == 0:
            err = glGetProgramInfoLog(self.shader_program)
            print(f"Link error: {err}")
        
        glDeleteShader(self.vertex_shader)
        glDeleteShader(self.fragment_shader)
        

    def use(self):

        glUseProgram(self.shader_program)
    
    def set_uniform1f(self, name: str, val: float):
        glUniform1f(
            glGetUniformLocation(self.shader_program, name),
            val
        )

    def _compile_program(self, source: str, shader_type):
        program = glCreateShader(shader_type)
        glShaderSource(program, source)
        glCompileShader(program)

        success = glGetShaderiv(program, GL_COMPILE_STATUS)

        if success == 0:
            # compile error
            log = glGetShaderInfoLog(program)
            print(log)
        
        return program