
from pyglet.graphics.shader import Shader, ShaderProgram

vertex_source = """#version 420 core

    in vec2 translate;
    in vec4 colors;
    in vec3 tex_coords;
    in vec2 scale;
    in vec4 position;
    in float rotation;

    out vec4 vertex_colors;
    out vec3 texture_coords;

    uniform WindowBlock
    {
        mat4 projection;
        mat4 view;
    } window;

    mat4 m_trans_scale = mat4(1.0);
    mat4 m_rotation = mat4(1.0);

    void main()
    {
        m_trans_scale[3][0] = translate.x;
        m_trans_scale[3][1] = translate.y;
        m_trans_scale[0][0] = scale.x;
        m_trans_scale[1][1] = scale.y;
        m_rotation[0][0] =  cos(-radians(rotation));
        m_rotation[0][1] =  sin(-radians(rotation));
        m_rotation[1][0] = -sin(-radians(rotation));
        m_rotation[1][1] =  cos(-radians(rotation));
        gl_Position = window.projection * window.view * m_trans_scale * m_rotation * position;
        vertex_colors = colors;
        texture_coords = tex_coords;
    }
"""

fragment_source = """#version 420 core

    in vec4 vertex_colors;
    in vec3 texture_coords;

    out vec4 final_colors;

    layout(binding=0) uniform sampler2D sprite_texture;
    layout(binding=1) uniform sampler2D palette_texture;

    void main()
    {
        vec4 color = texture(sprite_texture, texture_coords.xy);
        vec4 pal_color = texture(palette_texture, color.xy);
        /*
        if( pal_color == vec4(0.0, 0.0, 0.0, 1.0) )
        {
            final_colors = vec4(1.0, 0.0, 0.0, 1.0);
        }
        else
        {
            final_colors = vec4(pal_color.rgb, color.a) * vertex_colors;
        }
        */
        final_colors = pal_color * vertex_colors;
        //final_colors = texture(palette_texture, texture_coords.x) * vertex_colors;
    }
"""

_vert_shader = Shader(vertex_source, 'vertex')
_frag_shader = Shader(fragment_source, 'fragment')

def make_program():
    return ShaderProgram(_vert_shader, _frag_shader)
