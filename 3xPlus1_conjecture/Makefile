# Create executable 3xPlus1
#
# This can be runned with
# $ make
#

TARGET = 3xPlus1
CC = gcc
CFLAGS = -Wall -Wextra -pedantic -Wconversion -O3 -g -fno-stack-protector -lgcc_s
LFLAGS = -lpthread

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) -o $@ $^ $(CFLAGS) $(LFLAGS)
