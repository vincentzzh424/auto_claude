import argparse
import subprocess
import os
import sys
import json
import re
import time
from datetime import datetime
from graphlib import TopologicalSorter

DEFAULT_LANGUAGE = "Python"

# ================= Configuration & Utilities =================

class ConsoleStyle:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    

def print_step(stage, msg):
    """Prints a stylized stage header and message to the console."""
    print(f"{ConsoleStyle.HEADER}[{datetime.now().strftime('%H:%M:%S')}] {ConsoleStyle.BLUE}== {stage} =={ConsoleStyle.ENDC}")
    print(f"{ConsoleStyle.GREEN}{msg}{ConsoleStyle.ENDC}\n")

def parse_json_file(filepath):
    """Safely reads and parses a JSON file, handling potential Markdown code blocks."""
    if not os.path.exists(filepath): 
        return None
    with open(filepath, 'r', encoding='utf-8') as f: 
        text = f.read()
    # Remove Markdown code block syntax if present
    text = re.sub(r'```json\s*|```', '', text)
    try: 
        return json.loads(text)
    except: 
        return None

def execute_claude_agent(prompt, context_files=[], allow_fail=False, max_retries=2):
    """
    Invokes the Claude CLI via a temporary instruction file to bypass shell length limits.
    """
    # 1. Build context from files
    context_str = ",".join(context_files)
    
    # 2. Construct the massive system instruction
    massive_prompt_content = f"""
    [SYSTEM INSTRUCTION]
    You are a HEADLESS, NON-CONVERSATIONAL software agent.
    1. DO NOT talk. DO NOT explain.
    2. Read the instructions below and EXECUTE them immediately using tools.
    
    [CONTEXT FILES]
    {context_str}
    
    [USER TASK]
    {prompt}
    """
    
    # 3. Write instruction to a buffer file
    temp_instruction_file = "_claude_instruction_buffer.txt"
    with open(temp_instruction_file, "w", encoding="utf-8") as f:
        f.write(massive_prompt_content)
        
    print(f"🤖 (Instructions written to {temp_instruction_file}, Size: {len(massive_prompt_content)} chars)")
    
    # 4. Trigger Claude to read the buffer file
    trigger_prompt = f"Read the file '{temp_instruction_file}' and execute the [USER TASK] inside it immediately. Do not converse."
    
    cmd = [
        "claude", 
        "--dangerously-skip-permissions", 
        "-p", trigger_prompt ,"--verbose"
    ]
    
    is_windows = (os.name == 'nt')
    
    for attempt in range(max_retries + 1):
        try:
            subprocess.run(cmd, check=True, shell=is_windows)
            
            # Optional: Clean up buffer file
            # if os.path.exists(temp_instruction_file):
            #     os.remove(temp_instruction_file)
            return 
            
        except subprocess.CalledProcessError:
            if attempt < max_retries:
                print(f"{ConsoleStyle.YELLOW}⚠️ Claude failed, retrying ({attempt+1}/{max_retries})...{ConsoleStyle.ENDC}")
                time.sleep(3)
            else:
                if not allow_fail:
                    sys.exit(1)

# ================= STAGE -1: Requirement Research =================

def stage_requirement_research(raw_idea):
    print_step("STAGE -1", "Requirement Research & Analysis (Researcher)")

    prompt = f"""
    [ROLE]: Senior Product Researcher
    [IDEA]: {raw_idea}
    [LANGUAGE]: USE IDEA SAME LANGUAGE

    Please conduct comprehensive requirement research and analysis for this idea.

    RESEARCH SCOPE:
    1. **Market Research**: Identify similar products, competitors, and market trends
    2. **User Analysis**: Define target users, user personas, and use cases
    3. **Technical Feasibility**: Identify technical challenges, required technologies, and potential solutions
    4. **Best Practices**: Research industry standards, design patterns, and best practices for similar systems
    5. **Potential Risks**: Identify technical, business, and implementation risks
    6. **Feature Prioritization**: Suggest MVP features vs. future enhancements based on research

    OUTPUT REQUIREMENTS:
    - Generate `research.md` with all research findings
    - Include citations or references to industry standards where applicable
    - Provide actionable insights that will guide product design

    NOTE: This is RESEARCH phase. Do NOT write code or design the system yet. Focus on gathering information and insights.
    """
    execute_claude_agent(prompt)

# ================= STAGE -0.5: Brainstorming & User Scenarios =================

def stage_brainstorming(raw_idea):
    print_step("STAGE -0.5", "User Brainstorming & Scenario Design (User Personas)")

    prompt = f"""
    [ROLE]: User Experience Researcher & Scenario Designer
    [IDEA]: {raw_idea}
    [LANGUAGE]: USE IDEA SAME LANGUAGE
    [CONTEXT]: Based on research findings from `research.md`

    Conduct a multi-perspective brainstorming session by role-playing different target user personas.

    OUTPUT REQUIREMENTS:
    Generate `BRAIN.md` with the following sections:

    1. **User Personas** (3-5 distinct personas):
       - Name, age, occupation
       - Technical proficiency level
       - Primary goals and pain points
       - Attitude toward the product concept

    2. **Brainstorming Discussion**:
       - Simulated dialogue between personas discussing the idea
       - Each persona brings their unique perspective
       - Conflicts, agreements, and insights from the discussion
       - Different expectations and use cases emerge

    3. **User Scenarios** (5-8 scenarios):
       - For each scenario: context, motivation, expected outcome
       - Cover different personas and use cases
       - Include edge cases and unusual situations

    4. **Requirements List from User Perspectives**:
       - Must-have requirements (pain points that must be solved)
       - Nice-to-have features (delighters)
       - Anti-requirements (things users explicitly don't want)

    5. **Ideal Future Scenarios**:
       - Describe 2-3 "perfect world" scenarios where the product exceeds expectations
       - What would delight users beyond basic functionality
       - Long-term vision possibilities

    CRITICAL: This brainstorming should feel REAL. Each persona should have a distinct voice, real concerns, and valid perspectives. The discussion should reveal insights that wouldn't be obvious from a single perspective.

    NOTE: Do NOT write code. Only produce the BRAIN.md documentation.
    """
    execute_claude_agent(prompt, context_files=["research.md"])

# ================= STAGE 0: Product Definition =================

def stage_product_definition(raw_idea):
    print_step("STAGE 0", "Product Requirement Analysis (PM)")

    prompt = f"""
    [ROLE]: Senior Product Manager (PM)
    [IDEA]: {raw_idea}
    [LANGUAGE]: USE IDEA SAME LANGUAGE

    Please perform a deep requirement analysis on this idea, BASED on the research findings AND user brainstorming insights.

    OUTPUT REQUIREMENTS:
    1. `PRD.md` (Product Requirement Doc): Detailed feature list, tech stack confirmation (Default: {DEFAULT_LANGUAGE}).
       - MUST incorporate insights and findings from `research.md`
       - MUST leverage user personas, scenarios, and requirements from `BRAIN.md`
       - Align product features with research-backed user needs
       - Prioritize features based on user persona discussions
       - Consider technical feasibility identified in research
    2. `DATA_FLOW.md` (Data Flow Design): Data flow diagrams and core data structures.
       - Design data flows considering technical constraints from research
       - Consider user journey scenarios from BRAIN.md

    CRITICAL: Your PRD should be grounded in both the research findings from `research.md` AND the user insights from `BRAIN.md`. Leverage the market analysis, user personas, technical feasibility insights, and multi-perspective brainstorming to create a well-informed product specification.

    NOTE: Do NOT write code yet. Only produce documentation.
    """
    execute_claude_agent(prompt, context_files=["research.md", "BRAIN.md"])

# ================= STAGE 1: System Architecture =================

def stage_system_architecture():
    print_step("STAGE 1", "System Architecture & CLI Design (Architect)")
    
    prompt = f"""
    [ROLE]: System Architect
    [TASK]: Design the code architecture based on the PRD.
    [LANGUAGE]: USE PRD.md SAME LANGUAGE
    
    Read `PRD.md` and `DATA_FLOW.md`.
    
    OUTPUT REQUIREMENTS:
    1. Generate `architecture.json`.
       **CRITICAL**: Even if this is a Web Project, it must be a "CLI-First" architecture.
       The `entry_point` must handle command-line arguments to invoke underlying services directly for testing.
       
       Format Example:
       {{
           "modules": {{ ... }},
           "entry_point": "main.py",
           "cli_design": {{
               "run_server": "Start main service/web server",
               "test_api": "Call API function directly via JSON args (No network)",
               "inspect_db": "Print DB stats"
           }}
       }}
       
    2. Generate `requirements.txt` and install dependencies.
    """
    execute_claude_agent(prompt, context_files=["PRD.md", "DATA_FLOW.md"])

# ================= STAGE 2: Dependency Analysis =================

def stage_dependency_analysis():
    print_step("STAGE 2", "Compute Development Path (Topological Sort)")
    
    arch = parse_json_file("architecture.json")
    if not arch:
        print("❌ Unable to read architecture.json. Check Stage 1 output.")
        sys.exit(1)
        
    modules = arch.get('modules', {})
    sorter = TopologicalSorter()
    
    for name, info in modules.items():
        sorter.add(name, *info.get('dependencies', []))
    
    try:
        build_order = list(sorter.static_order())
        print(f"🔨 Build Order: {' -> '.join(build_order)}")
        return build_order, arch
    except Exception as e:
        print(f"{ConsoleStyle.FAIL}❌ Circular Dependency Error: {e}{ConsoleStyle.ENDC}")
        sys.exit(1)

# ================= STAGE 3: Development Loop =================

def stage_development_loop(build_order, arch_data):
    """
    Core CI/CD Loop: Develop -> Integrate -> Verify
    """
    modules_info = arch_data['modules']
    entry_point = arch_data.get('entry_point', 'main.py')
    
    completed_modules = [] 
    
    for module_name in build_order:
        if module_name not in modules_info: continue
        
        info = modules_info[module_name]
        
        # --- Step 3.1: Build (Dev) ---
        print_step("STAGE 3.1 (Dev)", f"Building Module: {module_name}")
        build_single_module(module_name, info)
        
        completed_modules.append(module_name)
        
        # --- Step 3.2: Integrate (Ops) ---
        print_step("STAGE 3.2 (Integration)", f"Integrating {module_name} into {entry_point}")
        integrate_module_into_entry(entry_point, completed_modules)
        
        # --- Step 3.3: Verify (QA) ---
        print_step("STAGE 3.3 (Verification)", f"Verifying {module_name} via CLI")
        verify_module_via_cli(entry_point, module_name)

def build_single_module(name, info):
    prompt = f"""
    [ROLE]: Senior {DEFAULT_LANGUAGE} Developer
    [DOCS]: PRD.md
    [ARCH]: architecture.json
    [TASK]: Develop the module `{name}` defined in modules.
    [COMMENT LANGUAGE]: USE PRD.md SAME LANGUAGE
    
    REQUIREMENTS:
    1. **NO MOCK**: Dependencies are ready. Import and use them directly.
    2. **IMPLEMENTATION**: Write real, robust code.
    3. **UNIT TEST**: Write `tests/test_{name}.py` and execute it to ensure it passes.
    """
    execute_claude_agent(prompt)

def integrate_module_into_entry(entry_point, completed_modules_list):
    """
    Updates the main entry point incrementally.
    """
    prompt = f"""
    [ROLE]: Integration Engineer
    [TASK]: Update the entry point file `{entry_point}`
    [DOCS]: PRD.md
    [ARCH]: architecture.json
    [COMMENT LANGUAGE]: USE PRD.md SAME LANGUAGE
    [READY MODULES]: {completed_modules_list}
    
    INSTRUCTIONS:
    1. Use `argparse` for CLI routing.
    2. **ONLY Import and Register functionality from [READY MODULES].** Do NOT import modules that are not built yet.
    3. Ensure Test Mode support: e.g., `python {entry_point} test --target [function] --args [json]`.
    4. Expose at least one core testable function for the latest module.
    """
    execute_claude_agent(prompt)

def verify_module_via_cli(entry_point, module_name):
    """
    Acceptance test for the new module via the CLI entry point.
    """
    prompt = f"""
    [ROLE]: QA Engineer and Senior {DEFAULT_LANGUAGE} Developer
    [DOCS]: PRD.md
    [ARCH]: architecture.json
    [COMMENT LANGUAGE]: USE PRD.md SAME LANGUAGE
    [TASK]: Verify that `{module_name}` is successfully integrated into `{entry_point}` and Fix exist bugs.
    
    INSTRUCTIONS:
    1. Construct a {DEFAULT_LANGUAGE} CLI command. Example: `python {entry_point} test --target [belonging_to_{module_name}] ...`
    2. Execute the command.
    3. Confirm the output is correct (Exit Code 0 and valid JSON/Text output).
    """
    execute_claude_agent(prompt)

# ================= STAGE 4: Refactoring & Review =================

def stage_refactoring(arch_data):
    print_step("STAGE 4", "System Refactoring & Code Review (Refactoring Lead)")

    prompt = f"""
    [ROLE]: System Refactoring Lead
    [TASK]: Review code design, simplify unreasonable modules, and ensure a solid foundation.
    [DOCS]: PRD.md
    [ARCH]: architecture.json
    [COMMENT LANGUAGE]:USE PRD.md SAME LANGUAGE
    
    EXECUTION STEPS:
    1. READ and ANALYZE the provided source files.
    2. IDENTIFY 1-3 specific areas for improvement (e.g., duplicated logic, messy imports, hardcoded values).
    3. REFACTOR (Rewrite) the code to be cleaner and more professional.
    4. **CRITICAL**: After refactoring, you MUST run project tests (e.g., `pytest` or `python main.py test`) to ensure functionality is intact.
    
    [SAFETY RULE]
    If tests fail after your refactor, you MUST fix the code immediately.
    
    EXECUTE REFACTORING NOW.
    """
    execute_claude_agent(prompt)

# ================= STAGE 5: Final Acceptance =================

def stage_final_acceptance(entry_point):
    print_step("STAGE 5", "Final System Acceptance Test")
    
    prompt = f"""
    [ROLE]: Acceptance Test Lead
    [TASK]: End-to-End System Test
    [DOCS]: PRD.md
    [LANGUAGE]: USE PRD.md SAME LANGUAGE
    
    All modules are developed and integrated. Verify their collaboration.
    
    INSTRUCTIONS:
    1. Run the project using standard {DEFAULT_LANGUAGE} commands (e.g., `python {entry_point} run`).
    2. Or run a complex test command involving multiple module interactions.
    3. Check for any remaining TODOs, 'Pass', or Mock code. Point them out or fix them.
    4. Output the final "PROJECT READY" confirmation.
    """
    execute_claude_agent(prompt)

# ================= Main Entry =================

def main():
    parser = argparse.ArgumentParser(description="Auto Claude - Autonomous Software Factory (CI/CD Edition)")
    parser.add_argument("raw_idea", help="The initial software idea or requirement")
    args = parser.parse_args()

    raw_idea = args.raw_idea
    print(f"Input Idea: {raw_idea}")

    # --- Pipeline Start ---

    # 0. Research Phase
    stage_requirement_research(raw_idea)

    # 0.5. Brainstorming Phase
    stage_brainstorming(raw_idea)

    # 1. Planning Phase
    stage_product_definition(raw_idea)
    stage_system_architecture() 
    
    # 2. Dependency Analysis
    build_order, arch_data = stage_dependency_analysis()
    
    # 3. Development Phase (Dev -> Integrate -> Verify Loop)
    stage_development_loop(build_order, arch_data)

    # 4. Refactoring Phase
    stage_refactoring(arch_data)
    
    # 5. Delivery Phase
    entry_point = arch_data.get('entry_point', 'main.py')
    stage_final_acceptance(entry_point)
    
    print_step("DONE", "✅ Project Construction Complete. All modules integrated and tested.")

if __name__ == "__main__":
    main()