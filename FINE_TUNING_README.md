# 🦁 LMU Buddy Fine-tuning with Ollama

This guide will help you fine-tune an Ollama model for your LMU Buddy project using the conversational data you provided. The fine-tuned model will have the personality and knowledge specific to LMU campus life.

## 📋 Overview

The fine-tuning process creates a custom LMU Buddy model that:
- ✅ Avoids repetitive/static responses
- ✅ Provides personalized, contextual responses
- ✅ Uses casual, student-friendly language
- ✅ Includes LMU-specific knowledge and locations
- ✅ Handles interactive features and feedback collection
- ✅ Gracefully handles edge cases

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
python setup_fine_tuning.py
```

This script will:
1. Check your Python version
2. Install required dependencies
3. Install Ollama (if not already installed)
4. Run the fine-tuning process
5. Test the integration

### Option 2: Manual Setup

If you prefer to run each step manually:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Ollama (if not already installed)
# Linux/macOS: curl -fsSL https://ollama.ai/install.sh | sh
# Windows: Download from https://ollama.ai/

# 3. Run fine-tuning
python fine_tune_lmu_buddy.py

# 4. Test the model
python lmu_buddy_ollama_client.py
```

## 📁 Generated Files

After running the fine-tuning process, you'll have these files:

- **`Modelfile`** - Ollama model configuration with system prompt and training examples
- **`lmu_buddy_training_data.json`** - Structured training data from your conversational examples
- **`lmu-buddy`** - Your fine-tuned Ollama model (accessible via `ollama list`)

## 🧪 Testing Your Model

### Direct Testing

Test the model directly with Ollama:

```bash
# Basic usage
ollama run lmu-buddy "Where should I eat on campus?"

# Interactive mode
ollama run lmu-buddy
```

### Integration Testing

Test the integration with your Streamlit app:

```bash
python lmu_buddy_ollama_client.py
```

### Streamlit App Integration

The fine-tuned model is automatically integrated into your Streamlit app. Just run:

```bash
streamlit run app.py
```

## 🎯 Training Data Overview

The fine-tuning uses your provided conversational examples organized into categories:

### 1. Avoid Repetitive/Static Responses
- Multiple response variations for "Where should I eat on campus?"
- Each response has different context and personality

### 2. Deepen Personalization & Context
- Coffee spot recommendations with time-based context
- Personalized responses with user name references
- Weather and location-specific study recommendations

### 3. Interactive Event Actions
- Event suggestions with follow-up actions
- Calendar integration prompts
- RSVP and reminder functionality

### 4. Enhanced Visual Feedback
- Welcome messages with confetti effects
- Feedback collection prompts
- Rating system integration

### 5. Feedback Collection
- Positive and negative feedback handling
- Rating collection prompts
- Improvement suggestions

### 6. Waitlist & Social Loop
- Beta feature access prompts
- Email collection for updates
- Social sharing incentives

### 7. Richer Example Prompts
- Dynamic question suggestions
- Campus-specific query examples
- Fun and engaging prompt variations

### 8. Edge Case Handling
- Unknown information graceful handling
- Official resource linking
- Creator feedback submission

### 9. LMU Buddy Personality
- Campus insider knowledge
- Humorous and relatable responses
- LMU-specific references and locations

## 🔧 Customization

### Adding More Training Data

To add more training examples, edit the `create_training_data()` method in `fine_tune_lmu_buddy.py`:

```python
conversations = [
    # Add your new conversations here
    {
        "prompt": "Your new prompt",
        "response": "Your new response"
    },
    # Or with multiple response variations
    {
        "prompt": "Your prompt",
        "responses": [
            "Response variation 1",
            "Response variation 2",
            "Response variation 3"
        ]
    }
]
```

### Changing the Base Model

You can change the base model by modifying the `base_model` parameter:

```python
fine_tuner = LMUBuddyFineTuner(
    base_model="llama2:13b",  # Larger model for better performance
    model_name="lmu-buddy"
)
```

Available base models:
- `llama2:7b` - Good balance of performance and speed
- `llama2:13b` - Better performance, slower inference
- `mistral:7b` - Alternative base model
- `codellama:7b` - Good for technical questions

### Modifying the System Prompt

Edit the `_get_system_prompt()` method to change the model's personality and knowledge:

```python
def _get_system_prompt(self) -> str:
    return """Your custom system prompt here..."""
```

## 🚨 Troubleshooting

### Common Issues

**1. Ollama not found**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

**2. Model creation fails**
```bash
# Check available models
ollama list

# Pull base model if needed
ollama pull llama2:7b

# Recreate the model
python fine_tune_lmu_buddy.py
```

**3. Slow responses**
```bash
# Use a smaller base model
# Edit fine_tune_lmu_buddy.py to use llama2:7b instead of llama2:13b
```

**4. Integration errors**
```bash
# Check if Ollama service is running
curl http://localhost:11434/api/tags

# Restart Ollama service
ollama serve
```

### Performance Optimization

**For faster inference:**
- Use `llama2:7b` as base model
- Ensure sufficient RAM (8GB+ recommended)
- Use SSD storage for model files

**For better quality:**
- Use `llama2:13b` as base model
- Add more training examples
- Refine the system prompt

## 📊 Model Performance

### Expected Behavior

After fine-tuning, your model should:

✅ **Provide varied responses** to the same question
✅ **Use casual, student-friendly language**
✅ **Reference LMU-specific locations and events**
✅ **Handle interactive features gracefully**
✅ **Collect feedback appropriately**
✅ **Maintain consistent personality**

### Quality Metrics

Monitor these aspects:
- **Response variety** - Different responses for similar questions
- **Context awareness** - Appropriate responses based on time/location
- **Personality consistency** - Maintains LMU Buddy character
- **Error handling** - Graceful handling of unknown queries

## 🔄 Updating the Model

To update your model with new training data:

1. **Add new conversations** to the training data
2. **Remove the old model**:
   ```bash
   ollama rm lmu-buddy
   ```
3. **Recreate the model**:
   ```bash
   python fine_tune_lmu_buddy.py
   ```

## 📚 Additional Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [LMU Campus Information](https://www.lmu.edu/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [LangChain Documentation](https://python.langchain.com/)

## 🤝 Contributing

To improve the fine-tuning:

1. **Add more training examples** based on user feedback
2. **Refine the system prompt** for better personality
3. **Test with different base models** for optimal performance
4. **Collect user feedback** to identify areas for improvement

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs in the terminal output
3. Ensure Ollama is properly installed and running
4. Verify all dependencies are installed

---

**Happy fine-tuning! 🦁✨**

Your LMU Buddy model will bring the roar back to campus with personalized, engaging responses that capture the true LMU spirit!