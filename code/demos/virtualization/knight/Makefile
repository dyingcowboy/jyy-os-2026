include ../../../mk/demo.mk

CXXFLAGS := -Wall -g -std=c++20

SRCS := $(wildcard *.cc)
OBJS := $(SRCS:.cc=)

# Default target
all: $(OBJS)

%: %.cc
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -f $(OBJS)

.PHONY: all clean
