// Author @patriciogv - 2015
// http://patriciogonzalezvivo.com

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

vec3 drawGear(vec2 pos, float offset, vec3 color)
{
	vec3 gear = vec3(0.0);
    //vec2 pos1 = vec2(0.5)-st;
    float r = length(pos)*2.0;
    float a = atan(pos.y,pos.x);
    float f = smoothstep(-0.468,0.608, cos(a*10.0+offset) )*-0.048+0.284;
    gear = vec3( 1.-smoothstep(f,f+0.02,r) );
    return gear * color;
}

void main(){
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    vec3 color = vec3(0.0);
	float offset = u_time * 2.0;
    
    vec2 pos1 = vec2(0.5)-st;
    vec2 pos2 = vec2(0.77,0.500)-st;
    vec2 pos3 = vec2(0.495, 0.77)-st;
    vec2 pos4 = vec2(0.325, 0.296)-st;
    vec2 pos5 = vec2(0.774,0.23)-st;
    vec2 pos6 = vec2(0.257,0.9)-st;
    
    vec3 color1 = vec3(0.831,1.000,0.567);
    vec3 color2 = vec3(1.000,0.350,0.926);
    
   
    
	vec3 gear1 = drawGear(pos1, offset, color1);
    vec3 gear2 = drawGear(pos2, -offset + 2.880, color2);
    vec3 gear3 = drawGear(pos3, -offset + 2.872, color2);
    vec3 gear4 = drawGear(pos4, -offset + 4.864, color2);
    vec3 gear5 = drawGear(pos5, offset + 6.272, color1);
    vec3 gear6 = drawGear(pos6, offset + 3.888, color1);

	color = gear1 + gear2 + gear3 + gear4 + gear5 + gear6;
    
    
    gl_FragColor = vec4(color, 1.0);
}
