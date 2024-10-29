from langchain.llms import MetaAI

# Load the template
with open('morning_weather_report_template.txt', 'r') as file:
    template = file.read()

# Initialize the MetaAI model
model = MetaAI()

# Generate the morning weather report
morning_weather_report = model.generate(template)
print('a')

# Print the generated report
print(morning_weather_report)
