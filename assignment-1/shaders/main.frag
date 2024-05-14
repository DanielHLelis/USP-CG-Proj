#version 410

in vec2 tex_coord;

uniform vec4 u_color;
uniform vec4 u_texture_filter;
uniform sampler2D texture_data;

out vec4 fragColor;

void main() {
  vec4 texel = texture(texture_data, tex_coord) * u_texture_filter + u_color;

  if (texel.a < 0.5) discard;

  fragColor = texel;
}
