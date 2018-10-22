#include "stdafx.h"
#include <iostream>
#include "OUI.h"

#define _DEBUG

int main()
{
	try {

		oui::Context context;

		oui::initialize();

		oui::Window* window = new oui::Window();
		window->setName("original");
		window->setTitle(u"Falling Dots");

		window->addOSALStyle(u"data/page.osal");

		oui::ComponentLoader cl;
		cl.loadComponents(u"data/page.oui");
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
		
		context.addWindow(window);
		

		while(true) {

			if(context.process() == -1) {
				break;
			}

			oui::sleep(4);
		}
	} catch(char* error) {
		std::cout << "Error: " << error << std::endl;
	}
    return 0;
}

