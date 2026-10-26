#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <stdio.h>

static const char *vert_src =
    "#version 330 core\n"
    "const vec2 pos[3] = vec2[3](vec2(-1,-1), vec2(3,-1), vec2(-1,3));\n"
    "void main() { gl_Position = vec4(pos[gl_VertexID], 0, 1); }\n";

static const char *frag_src =
    "#version 330 core\n"
    "uniform vec2 u_resolution;\n"
    "uniform float u_time;\n"
    "out vec4 frag_color;\n"
    "void main() {\n"
    "    vec2 uv = gl_FragCoord.xy / u_resolution;\n"
    "    float d = length(uv - 0.5);\n"
    "    float c = 0.5 + 0.5 * sin(d * 20.0 - u_time * 3.0);\n"
    "    frag_color = vec4(vec3(c * uv, 1.0 - c), 1.0);\n"
    "}\n";

static GLuint compile(GLenum type, const char *src) {
    GLuint s = glCreateShader(type);
    glShaderSource(s, 1, &src, NULL);
    glCompileShader(s);
    GLint ok;
    glGetShaderiv(s, GL_COMPILE_STATUS, &ok);
    if (!ok) {
        char log[512];
        glGetShaderInfoLog(s, sizeof(log), NULL, log);
        fprintf(stderr, "shader error: %s\n", log);
    }
    return s;
}

int main(void) {
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow *win = glfwCreateWindow(640, 480, "shader", NULL, NULL);
    glfwMakeContextCurrent(win);
    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);

    GLuint prog = glCreateProgram();
    glAttachShader(prog, compile(GL_VERTEX_SHADER, vert_src));
    glAttachShader(prog, compile(GL_FRAGMENT_SHADER, frag_src));
    glLinkProgram(prog);

    GLuint vao;
    glGenVertexArrays(1, &vao);

    while (!glfwWindowShouldClose(win)) {
        int w, h;
        glfwGetFramebufferSize(win, &w, &h);
        glViewport(0, 0, w, h);
        glClear(GL_COLOR_BUFFER_BIT);

        glUseProgram(prog);
        glUniform2f(glGetUniformLocation(prog, "u_resolution"), (float)w, (float)h);
        glUniform1f(glGetUniformLocation(prog, "u_time"), (float)glfwGetTime());

        glBindVertexArray(vao);
        glDrawArrays(GL_TRIANGLES, 0, 3);

        glfwSwapBuffers(win);
        glfwPollEvents();
    }

    glfwTerminate();
    return 0;
}
