import ctypes
import glfw
import glm
from OpenGL.GL import *
import numpy as np
import imgui
from imgui.integrations.glfw import GlfwRenderer
from shader import ShaderProgram
from vol_parser import parse_vol_file


def read_program_source(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


class Window:

    def __init__(self) -> None:
        # Initialize imgui
        imgui.create_context()

        # Initialize the library
        if not glfw.init():
            return
        # Force core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # Create a windowed mode window and its OpenGL context
        window = glfw.create_window(640, 640, "Hello World", None, None)
        if not window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(window)

        self.impl = GlfwRenderer(window) 

        # read the volume data
        volume, dim_depth, dim_w, dim_h = parse_vol_file("Skull.vol")
        print(volume.shape)

        # vao
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)

        # vbo
        vbo = glGenBuffers(1)

        vertices = np.array([
            # x, y
            -1.0,  1.0,  # top left
            1.0,  1.0,  # top right
            1.0, -1.0,  # bottom right
            -1.0, -1.0,  # bottom left
        ], dtype=np.float32)

        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes,
                     vertices.data, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE,
                              2 * vertices.itemsize, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # ebo
        ebo = glGenBuffers(1)
        indices = np.array([
            0, 1, 2,  # first triangle
            0, 2, 3  # second triangle
        ], dtype=np.uint32)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes,
                     indices.data, GL_STATIC_DRAW)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_3D, texture)

        # Upload texture
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_3D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage3D(GL_TEXTURE_3D, 0, GL_RED, dim_w, dim_h,
                     dim_depth, 0, GL_RED, GL_UNSIGNED_BYTE, volume.data)

        self.shader = ShaderProgram(
            vertex_source=read_program_source("vertex_shader.vs"),
            fragment_source=read_program_source("fragment_shader.fs"))

        self.shader.use()

        # camera
        camera_pos = glm.vec3(0.0, 0.0, 0.0)

        glUniform3fv(
            glGetUniformLocation(self.shader.shader_program, "cameraPos"),
            1,
            glm.value_ptr(camera_pos)
        )

        deg = 0.0

        # params for shader
        delta = 0.01
        self.shader.set_uniform1f("delta", delta)
        stepSize = 0.01
        self.shader.set_uniform1f("stepSize", stepSize)
        tn = 0.0
        self.shader.set_uniform1f("tn", tn)
        tf = 5.0
        self.shader.set_uniform1f("tf", tf)

        # other parameters
        rotate_speed = 150

        self.last_time = glfw.get_time()


        # Loop until the user closes the window
        while not glfw.window_should_close(window):
            # Render here, e.g. using pyOpenGL

            current_time = glfw.get_time()
            delta_time = current_time - self.last_time

            t = glm.mat4(1.0)
            t = glm.rotate(t, glm.radians(deg), glm.vec3(0.0, 1.0, 0.0))
            t = glm.translate(t, glm.vec3(0.0, 0.0, 1.0))

            glUniformMatrix4fv(
                glGetUniformLocation(
                    self.shader.shader_program, "camTransform"),
                1,
                False,
                # glm.value_ptr(self.camera.cam_to_world_matrix())
                glm.value_ptr(t)
            )

            deg += rotate_speed * delta_time

            self.shader.use()
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT,
                           ctypes.c_void_p(0))
            # draw UI
            imgui.new_frame()
            imgui.begin("Config", True)
            changed, v = imgui.slider_float("delta", delta, max_value=5.0, min_value=0.001)
            if changed:
                self.shader.set_uniform1f("delta", v)
                delta = v

            changed, v = imgui.slider_float("stepSize", stepSize, max_value=0.5, min_value=0.001)
            if changed:
                self.shader.set_uniform1f("stepSize", v)
                stepSize = v

            changed, v = imgui.slider_float("tn", tn, max_value=5.0, min_value=0.0)
            if changed:
                self.shader.set_uniform1f("tn", v)
                tn = v

            changed, v = imgui.slider_float("tf", tf, max_value=5.0, min_value=0.0)
            if changed:
                self.shader.set_uniform1f("tf", v)
                tf = v

            changed, v = imgui.slider_int("rotate speed", rotate_speed, max_value=300, min_value=0)
            if changed:
                rotate_speed = v
            imgui.end()

            # imgui.show_demo_window()

            imgui.render()
            self.impl.render(imgui.get_draw_data())

            # Swap front and back buffers
            glfw.swap_buffers(window)

            # Poll for and process events
            glfw.poll_events()
            # Imgui
            self.impl.process_inputs()
            self.last_time = current_time

        glfw.terminate()


if __name__ == "__main__":
    Window()
