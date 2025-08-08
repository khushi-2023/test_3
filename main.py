from asr_engine import hybrid_asr
from nlp_parser import parse_git_command
from git_executor import execute_git_commands
from voice_feedback import speak, log_command

print("🚀 Voice-Git Automation Started")
speak("Please say offline or online to select ASR mode")

# ✅ Voice-based mode selection loop
while True:
    print("🎤 Please say 'offline' or 'online' to select ASR mode...")
    mode = hybrid_asr("online").lower().strip()  # Always use online for mode selection
    print(f"🎤 Recognized (Mode Selection): {mode}")

    if "offline" in mode:
        mode = "offline"
        print("✅ Selected ASR Mode: Offline")
        speak("Selected ASR Mode: Offline")
        break
    elif "online" in mode:
        mode = "online"
        print("✅ Selected ASR Mode: Online")
        speak("Selected ASR Mode: Online")
        break
    else:
        print("❌ Couldn't detect mode. Please say 'offline' or 'online'.")
        speak("I could not detect the mode. Please say offline or online.")

# ✅ Main Voice Command Loop
try:
    while True:
        text = hybrid_asr(mode)
        if not text:
            continue

        print(f"🎤 [{mode.capitalize()} Mode] Recognized: {text}")

        # ✅ Exit command
        if text.lower() in ["exit", "quit", "stop", "close"]:
            print("👋 Exiting Voice-Git Automation. Goodbye!")
            speak("Exiting Voice Git Automation. Goodbye!")
            break

        commands = parse_git_command(text)

        if commands[0] == "Unknown command":
            print("❌ Unknown Git command. Please try again.")
            speak("Unknown Git command. Please try again.")
            continue

        log_command(text)
        speak(f"Executing {', '.join(commands)}")
        execute_git_commands(commands)
        print("✅ Command executed successfully.")
        speak("Command executed successfully.")

except KeyboardInterrupt:
    print("\n👋 Exiting Voice-Git Automation (Keyboard Interrupt).")
    speak("Exiting Voice Git Automation. Goodbye!")
