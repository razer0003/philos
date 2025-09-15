#!/usr/bin/env python3

from ai_companion import AICompanion

# Test with mock GUI object
class MockGUI:
    def __init__(self):
        self.show_internal_monologue = False

def test_token_optimization():
    print('=== Testing Token Optimization ===')
    
    # Create mock GUI and AI companion
    mock_gui = MockGUI()
    ai = AICompanion()
    ai.set_gui_reference(mock_gui)

    try:
        # Test 1: Internal monologue disabled
        print('\nTest 1: Internal monologue DISABLED')
        response = ai.interact('Hello there!')
        internal_monologue = response.get('internal_monologue', '')
        
        if not internal_monologue:
            print('✓ SUCCESS: Internal monologue skipped when GUI disabled')
            print('✓ Tokens saved!')
        else:
            print('✗ FAILED: Internal monologue generated even when disabled')
            print(f'Generated: "{internal_monologue}"')
        
        print(f'Internal monologue value: "{internal_monologue}"')
        
        # Test 2: Internal monologue enabled
        print('\nTest 2: Internal monologue ENABLED')
        mock_gui.show_internal_monologue = True
        response2 = ai.interact('Hello again!')
        internal_monologue2 = response2.get('internal_monologue', '')
        
        if internal_monologue2:
            print('✓ SUCCESS: Internal monologue generated when GUI enabled')
            print(f'Generated content length: {len(internal_monologue2)} characters')
        else:
            print('✗ FAILED: No internal monologue when should be enabled')
        
        print(f'Internal monologue content: "{internal_monologue2[:100]}..."')
        
        # Test 3: Back to disabled
        print('\nTest 3: Internal monologue DISABLED again')
        mock_gui.show_internal_monologue = False
        response3 = ai.interact('Final test message')
        internal_monologue3 = response3.get('internal_monologue', '')
        
        if not internal_monologue3:
            print('✓ SUCCESS: Internal monologue skipped after re-disabling')
        else:
            print('✗ FAILED: Internal monologue still generating after disable')
        
        print(f'Final internal monologue: "{internal_monologue3}"')
        
        print('\n=== Token Optimization Test Complete ===')
        
    except Exception as e:
        print(f'Error during testing: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_token_optimization()