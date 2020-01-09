"""
Simple shaders used for drawing polygons.
"""

from pyglet.gl import *
import pyglet
import glm


vertex_src = """#version 330 core
    in vec4 vertices;
    in vec4 colors;
    in vec2 tex_coords;

    out vec4 vertex_colors;
    out vec2 texture_coords;

    uniform WindowBlock
    {
        mat4 projection;
        mat4 view;
    } window;

    void main()
    {
        gl_Position = window.projection * window.view * vertices;

        vertex_colors = colors;
        texture_coords = tex_coords;
    }
"""

fragment_src = """#version 330 core
    in vec4 vertex_colors;
    in vec2 texture_coords;

    out vec4 final_colors;

    void main()
    {
        final_colors = vertex_colors;
    }
"""

_vert_shader = pyglet.graphics.shader.Shader(vertex_src, "vertex")
_frag_shader = pyglet.graphics.shader.Shader(fragment_src, "fragment")

program = pyglet.graphics.shader.ShaderProgram(_vert_shader, _frag_shader)
