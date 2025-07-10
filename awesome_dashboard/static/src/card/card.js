/** @odoo-module **/

import { Component, useState } from "@odoo/owl";

export class DashboardItem extends Component {
    static template = "awesome_owl.DashboardItem";

    static props = {
        size: {type: Number},

        slots: {
            type: Object,
            shape: {
                default: true
            },
        }
    };

    setup() {

    }

}
