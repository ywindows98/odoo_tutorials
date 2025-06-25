/** @odoo-module **/

import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { TodoItem } from "./todo_item";

export class TodoList extends Component {
    static template = "awesome_owl.TodoList";
    static components = { TodoItem };

    setup() {
//        this.todos = useState([
//            { id: 3, description: "buy milk", isCompleted: true },
//            { id: 4, description: "sell milk", isCompleted: false }
//        ]);
        this.nextId = 0;
        this.todos = useState([]);

        this.inputRef = useRef('todo_input');
        onMounted(() => {
           console.log(this.inputRef.el);
        });
    }

    addTodo(ev) {
        if(ev.keyCode === 13 && ev.target.value != ""){
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false
            })

            ev.target.value = "";
        }
    }

}
