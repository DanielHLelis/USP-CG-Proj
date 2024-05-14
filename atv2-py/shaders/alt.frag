#version 410

out vec4 fragColor;

uniform vec4 u_color;
uniform vec4 u_texture_filter;

void main() {
    fragColor = vec4(1.0, 0.0, 0.0, 0.6);
}
