include ../../../mk/demo.mk

CFLAGS   := -O2 $(PTHREAD)
CXXFLAGS := -O2 -std=c++20

SRCS := $(wildcard *.c)
CXXS := $(wildcard *.cpp)
OBJS := $(SRCS:.c=) $(CXXS:.cpp=)

# Default target
all: $(OBJS)

%: %.c
	$(CC) $(CFLAGS) $< -o $@

%: %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -f $(OBJS)

.PHONY: all clean
