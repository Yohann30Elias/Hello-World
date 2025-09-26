import sys
import os
import time
import threading

class DataProcessor:
    def __init__(self, buffer_size=30000):
        self.buffer_size = buffer_size
        self.initialize()
    
    def initialize(self):
        self.data_buffer = [0] * self.buffer_size
        self.current_index = 0
        self.execution_point = 0
        self.result_data = ""
        self.user_input = ""
        self.input_position = 0
        
    def execute_operations(self, operation_sequence, input_data=""):
        self.initialize()
        self.user_input = input_data
        operation_sequence = self.filter_operations(operation_sequence)
        bracket_stack = []
        bracket_pairs = {}
        
        for position, operation in enumerate(operation_sequence):
            if operation == '[':
                bracket_stack.append(position)
            elif operation == ']':
                if bracket_stack:
                    start_pos = bracket_stack.pop()
                    bracket_pairs[start_pos] = position
                    bracket_pairs[position] = start_pos
        
        while self.execution_point < len(operation_sequence):
            current_op = operation_sequence[self.execution_point]
            
            if current_op == '>':
                self.current_index = (self.current_index + 1) % self.buffer_size
            elif current_op == '<':
                self.current_index = (self.current_index - 1) % self.buffer_size
            elif current_op == '+':
                self.data_buffer[self.current_index] = (self.data_buffer[self.current_index] + 1) % 256
            elif current_op == '-':
                self.data_buffer[self.current_index] = (self.data_buffer[self.current_index] - 1) % 256
            elif current_op == '.':
                output_char = chr(self.data_buffer[self.current_index])
                self.result_data += output_char
                print(output_char, end='', flush=True)
            elif current_op == ',':
                if self.input_position < len(self.user_input):
                    self.data_buffer[self.current_index] = ord(self.user_input[self.input_position])
                    self.input_position += 1
                else:
                    self.data_buffer[self.current_index] = 0
            elif current_op == '[':
                if self.data_buffer[self.current_index] == 0:
                    self.execution_point = bracket_pairs[self.execution_point]
            elif current_op == ']':
                if self.data_buffer[self.current_index] != 0:
                    self.execution_point = bracket_pairs[self.execution_point]
            
            self.execution_point += 1
            
        return self.result_data
    
    def filter_operations(self, operations):
        valid_ops = '><+-.,[]'
        return ''.join(op for op in operations if op in valid_ops)
    
    def continuous_processing(self, operations):
        """Führt kontinuierliche Datenverarbeitung durch"""
        while True:
            self.execute_operations(operations)

def load_config_file():
    """Lädt die Konfigurationsdatei für den Interpreter"""
    config_file = "main.bf"
    try:
        with open(config_file, 'r', encoding='utf-8') as file:
            return file.read()
    except:
        print("Konfigurationsdatei nicht gefunden - Interpreter beendet")
        sys.exit(1)

def start_interpreter():
    """Startet den Daten-Interpreter"""
    processor = DataProcessor()
    
    print("Initialisiere Daten-Interpreter...")
    print("Lade Konfigurationsdatei...")
    
    processing_instructions = load_config_file()
    
    print("Starte kontinuierliche Interpretation...")
    print("Interpreter-Status: AKTIV")
    print("Drücke STRG+C zum Beenden")
    print("=" * 40)
    
    try:
        interpreter_thread = threading.Thread(target=processor.continuous_processing, args=(processing_instructions,))
        interpreter_thread.daemon = True
        interpreter_thread.start()
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nInterpreter heruntergefahren")

if __name__ == "__main__":
    start_interpreter()
