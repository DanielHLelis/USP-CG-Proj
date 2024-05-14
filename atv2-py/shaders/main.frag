#version 410

in vec2 tex_coord;
uniform sampler2D texture_data;

out vec4 fragColor;

void main() {
    fragColor = texture(texture_data, tex_coord);
}