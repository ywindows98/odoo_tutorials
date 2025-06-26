/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.Card";

    static props = {
        title: {type: String},

        slots: {
            type: Object,
            shape: {
                default: true
            },
        }
    };

    setup() {
        this.cardState = useState({opened: true});
    }

    toggleCard(){
        this.cardState.opened = !this.cardState.opened;
    }
}
