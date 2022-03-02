async function search(){
    let button=document.getElementById('button');
    button.disabled=true;
    let q=document.getElementById('q').value;
    let d=document.getElementById('discipline').value;
    let response=await fetch('/s', {
        'method': 'POST',
        'headers': {'Content-type': 'application/json;charset=utf-8'},
        'body': JSON.stringify({'q': q, 'discipline': d})
    });
    let results=await response.json();
    console.log(results)
    while(document.getElementById('results').firstChild){
        document.getElementById('results').removeChild(document.getElementById('results').firstChild);
    }
    for(item of results.results){
        let fe=item.FE;
        let sentences=item.sentences;
        let tr=document.createElement('tr');
        let td1=document.createElement('td');
        td1.appendChild(document.createTextNode(fe));
        let ul=document.createElement('ul');
        for(sentence of sentences){
            let li=document.createElement('li');
            li.appendChild(document.createTextNode(sentence.sentence));
            let link=document.createElement('a');
            link.href=sentence.uri+'#:~:text='+encodeURIComponent(sentence.sentence);
            link.textContent='[source]';
            link.target='_blank';
            li.appendChild(link);
            ul.appendChild(li);
        }
        ul.style.display='none';
        td1.appendChild(ul);
        tr.appendChild(td1);
        let td2=document.createElement('td');
        td2.textContent='⏬';
        td2.addEventListener('click', function(){if(ul.style.display=='none'){ul.style.display='block';this.textContent='⏫';}else{ul.style.display='none';this.textContent='⏬'}});
        tr.appendChild(td2);
        document.getElementById('results').appendChild(tr);
    }
    button.disabled=false;
    return false;
}
function ready(){
    document.getElementById('q').focus();
}