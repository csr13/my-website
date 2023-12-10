class ListFilter {
    constructor(listId) {
        this.list = document.getElementById(listId)
        this.searchField = this.list.children[0]
        this.listList = this.list.children[1]
        this.meta = {}
    }
    
    searchList(term) {
        var items = []
        Array.from(this.listList.children).forEach(function(i, x) {
            var tit = i.children[0].children[0].innerText.replace(/\d+\)\s/, "");
            if (tit.toLowerCase().match(term.toLowerCase()))
                items.push(tit)
        })
        return items
    }
    
    addSearchFieldEventListener() {
        this.searchField.addEventListener("input", (event) => {
            if (event.target.value == "")
                this.meta.originalList.forEach((i) => this.listList.append(i))
            var list = this.searchList(event.target.value);
            var toAdd = [];
            this.meta.originalList.forEach((i, x) => {
                var tit = i.children[0].children[0].innerText.replace(/\d+\)\s/, "");
                for (let a = 0; a < list.length ; a++)
                    if (list[a] == tit) toAdd.push(i);
            })
            for (let i = 0; i < this.listList.children.length; i++) 
                this.listList.children[0].remove();
             for (let i = 0; i < toAdd.length; i++) 
                this.listList.appendChild(toAdd[i])
        })
    }

    main() {
        this.meta.originalList = Array.from(this.listList.children);
        this.addSearchFieldEventListener()
    }
}
