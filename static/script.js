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
        tr.appendChild(td1);
        let td2=document.createElement('td');
        let a=document.createElement('a');
        a.appendChild(document.createTextNode('Examples'));
        a.target='_blank';
        a.href='https://scholar.google.com/scholar?q=%22'+fe.replace(/ /g, '+')+'%22';
        td2.appendChild(a);
        tr.appendChild(td2);
        document.getElementById('results').appendChild(tr);
    }
    button.disabled=false;
    return false;
}
function ready(){
    document.getElementById('q').focus();
}