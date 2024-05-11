attribute vec2 position;
uniform mat4 mat;

void main(){
    gl_Position = mat * vec4(position,0.0,1.0);
}