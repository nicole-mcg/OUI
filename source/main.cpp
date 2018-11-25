#include <iostream>
#include "OUI.h"

#include "libplatform/libplatform.h"
#include "v8.h"

#define _DEBUG

void testV8();

int main(int argc, char *argv[])
{
	try {
        long long v8Start = oui::currentTimeMillis();
        testV8();

		oui::initialize();

        std::cout << "V8 took " << (oui::currentTimeMillis() - v8Start) << "ms" << std::endl;
		oui::Context* context = oui::OS->createContext();

        long long ouiStart = oui::currentTimeMillis();

		oui::Window* window = context->createWindow(1366, 768);
		window->setName("original");
		window->setTitle(u"OUI Demo");

		window->addOSALStyle(u"./data/page.osal");

		oui::ComponentLoader cl;
		cl.loadComponents(u"./data/page.oui");
		
		oui::Panel* panel = cl.toPanel();
		window->addChild(panel);

		oui::Panel* drawPanel = (oui::Panel*) panel->getChild("panel");
		drawPanel->getChild("topBtn")->addEventListener(oui::Event::CLICKED, [](oui::MouseEvent e, oui::Component* c) {
			if (e.type == oui::Event::CLICKED) {
				c->getWindow()->getChildCont("loadedpanel")->getChild("container")->setAttribute("visible", true);
				c->getWindow()->getChildCont("loadedpanel")->getChild("panel")->setAttribute("visible", false);
			}
		});

		panel->getChildCont("container")->getChild("btn1")->addEventListener(oui::Event::CLICKED, [](oui::MouseEvent e, oui::Component* c) {
			c->getWindow()->getChildCont("loadedpanel")->getChild("panel")->setAttribute("visible", true);
			c->getWindow()->getChildCont("loadedpanel")->getChild("container")->setAttribute("visible", false);
		});

		const int BUTTON_LENGTH = 100;
		oui::Button** buttons = new oui::Button*[BUTTON_LENGTH];
		for (int i = 0; i < BUTTON_LENGTH; i++) {
			buttons[i] = NULL;
		}

		panel->getChildCont("container")->getChild("btn2")->addEventListener(oui::Event::CLICKED, [buttons, BUTTON_LENGTH](oui::MouseEvent e, oui::Component* c) {
			long long start = oui::currentTimeMillis();
			for (int i = 0; i < BUTTON_LENGTH; i++) {
				oui::Button* b = buttons[i] = new oui::Button(std::string("test").append(std::to_string(i)), "gameButton");
				b->setAttribute("width-offset", 100);
				b->setAttribute("height-offset", 20);
				b->setAttribute("x-percent", 50);
				b->setAttribute("y-offset", 20 + i * 35);
				b->setAttribute("text", u"btn" + intToString(i));
				c->getWindow()->getChildCont("loadedpanel")->getChildCont("container")->getChildCont("panel2")->addChild(buttons[i]);
			}

			std::cout << "added Buttons took: " << (oui::currentTimeMillis() - start) << "ms" << std::endl;
		});
        
		panel->getChildCont("container")->getChild("btn3")->addEventListener(oui::Event::CLICKED, [panel](oui::MouseEvent e, oui::Component* c) {
			if (e.type == oui::Event::CLICKED) {
				for (int i = 0; i < 100; i++) {
					c->getWindow()->getChildCont("loadedpanel")->getChildCont("container")->getChildCont("panel2")->removeAllChildren(true);
				}
				
			}
		});

		window->setVisible(true);
		
		context->addWindow(window);
		
        std::cout << "OUI took " << (oui::currentTimeMillis() - ouiStart) << "ms" << std::endl;


		while(true) {

			if(context->process() == -1) {
				break;
			}

			oui::sleep(4);
		}

        oui::shutdown();
	} catch(char* error) {
		std::cout << "Error: " << error << std::endl;
	}
    return 0;
}

void testV8() {
    // Initialize V8.
  v8::V8::InitializeICUDefaultLocation("OUI Runtime");
  v8::V8::InitializeExternalStartupData("OUI Runtime");
  std::unique_ptr<v8::Platform> platform = v8::platform::NewDefaultPlatform();
  v8::V8::InitializePlatform(platform.get());
  v8::V8::Initialize();

  // Create a new Isolate and make it the current one.
  v8::Isolate::CreateParams create_params;
  create_params.array_buffer_allocator =
      v8::ArrayBuffer::Allocator::NewDefaultAllocator();
  v8::Isolate* isolate = v8::Isolate::New(create_params);
  {
    v8::Isolate::Scope isolate_scope(isolate);

    // Create a stack-allocated handle scope.
    v8::HandleScope handle_scope(isolate);

    // Create a new context.
    v8::Local<v8::Context> context = v8::Context::New(isolate);

    // Enter the context for compiling and running the hello world script.
    v8::Context::Scope context_scope(context);

    {
      // Create a string containing the JavaScript source code.
      v8::Local<v8::String> source =
          v8::String::NewFromUtf8(isolate, "'Wow, this is the best tes!'",
                                  v8::NewStringType::kNormal)
              .ToLocalChecked();

      // Compile the source code.
      v8::Local<v8::Script> script =
          v8::Script::Compile(context, source).ToLocalChecked();

      // Run the script to get the result.
      v8::Local<v8::Value> result = script->Run(context).ToLocalChecked();

      // Convert the result to an UTF8 string and print it.
      v8::String::Utf8Value utf8(isolate, result);
      printf("%s\n", *utf8);
    }

    {
      // Use the JavaScript API to generate a WebAssembly module.
      //
      // |bytes| contains the binary format for the following module:
      //
      //     (func (export "add") (param i32 i32) (result i32)
      //       get_local 0
      //       get_local 1
      //       i32.add)
      //
      const char* csource = R"(
        let bytes = new Uint8Array([
          0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x07, 0x01,
          0x60, 0x02, 0x7f, 0x7f, 0x01, 0x7f, 0x03, 0x02, 0x01, 0x00, 0x07,
          0x07, 0x01, 0x03, 0x61, 0x64, 0x64, 0x00, 0x00, 0x0a, 0x09, 0x01,
          0x07, 0x00, 0x20, 0x00, 0x20, 0x01, 0x6a, 0x0b
        ]);
        let module = new WebAssembly.Module(bytes);
        let instance = new WebAssembly.Instance(module);
        instance.exports.add(3, 4);
      )";

      // Create a string containing the JavaScript source code.
      v8::Local<v8::String> source =
          v8::String::NewFromUtf8(isolate, csource, v8::NewStringType::kNormal)
              .ToLocalChecked();

      // Compile the source code.
      v8::Local<v8::Script> script =
          v8::Script::Compile(context, source).ToLocalChecked();

      // Run the script to get the result.
      v8::Local<v8::Value> result = script->Run(context).ToLocalChecked();

      // Convert the result to a uint32 and print it.
      uint32_t number = result->Uint32Value(context).ToChecked();
      printf("3 + 4 = %u\n", number);
    }
  }

  // Dispose the isolate and tear down V8.
  isolate->Dispose();
  v8::V8::Dispose();
  v8::V8::ShutdownPlatform();
  delete create_params.array_buffer_allocator;
}