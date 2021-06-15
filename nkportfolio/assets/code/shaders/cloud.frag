// Author @patriciogv - 2015
// http://patriciogonzalezvivo.com

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

float random (in vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(0.380,0.510)))*
        u_time);
}

// Based on Morgan McGuire @morgan3d
// https://www.shadertoy.com/view/4dS3Wd
float noise (in vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);

    // Four corners in 2D of a tile
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y;
}

#define OCTAVES 8
float fbm (in vec2 st) {
    // Initial values
    float value = -0.312;
    float amplitude = 0.644;
    float frequency = 2.072;
    //
    // Loop of octaves
    for (int i = 0; i < OCTAVES; i++) {
        value += amplitude * noise(st);
        st *= 2.;
        amplitude *= .5;
    }
    return value;
}

void main() {
    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    st.x *= u_resolution.x/u_resolution.y;

    vec3 color = vec3(0.331,0.595,0.228);
    vec3 color2 = vec3(0.144,0.275,0.355);
    
    color += fbm(st*sin(u_time/10.)*11.120);
    color += fbm(st*5.0);
    color2 += fbm(st*1.800);
    float mask = smoothstep(0.0, 1.0, st.y);
    color = color * mask;
    color2 *= 1.0 - mask;
	//color = smoothstep(vec3(0.350,0.350,0.350), color2, color);
    gl_FragColor = vec4(1.0-(color+color2),1.0);
}
