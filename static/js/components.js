const DEFAULT_LIST_LENGTH = 3;

function Item(props){
  if("content" in props){
    const item = props.content.item;
    const amount = props.content.quantity;
    return(<div className="row">
		<div className="input-field col s6">
        <input type="text" name="item" defaultValue={item} required/>
		</div>
		<div className="input-field col s6">
        <input type="text" name="quantity" defaultValue={amount} required/>
		</div>
        </div>);

  }else{
    return(<div className="row">
		<div className="input-field col s6">
		<input type="text" name="item" placeholder="材料名" required/>
		</div>
		<div className="input-field col s6">
		<input type="text" name="quantity" placeholder="数量" required/></div>
		</div>);
  }
}

class Itemlist extends React.Component {
  constructor(props){
    super(props);
    const hasContent = "content" in props;
    const l = [];
    if(hasContent){
      for(let i=0; i<props.content.length; i++){
        l.push(<Item content={props.content[i]}/>)
      }
    }else{
      for (let i = 0; i < 3; i++){
        l.push(<Item />);
      }
    }

    this.state={initialState: l, currentState: l, hasContent: hasContent};
    this.addItem = this.addItem.bind(this);
    this.removeItem = this.removeItem.bind(this);
    this.reset = this.reset.bind(this);
  }

  addItem(e){
    e.preventDefault();
    const currentState = this.state.currentState;
    const newState = currentState.concat([<Item />]);
    this.setState({currentState: newState});
  }

  removeItem(e){
    e.preventDefault();
    const currentState = this.state.currentState;
    if(currentState.length <= 1) return;
    const newState = currentState.slice(0,-1);
    this.setState({currentState: newState});
  }

  reset(e){
    e.preventDefault();
    const initialState = this.state.initialState;
    this.setState({currentState: initialState});
    var items = $("[name=item]");
    var amounts = $("[name=quantity]");
    if(this.state.hasContent){
        var loopLen = Math.min(items.length, this.props.content.length);
        for(let i=0;i<loopLen; i++){
            items[i].value = this.props.content[i].item;
            amounts[i].value = this.props.content[i].amount;
        }
    }else{
        var loopLen = Math.min(items.length, DEFAULT_LIST_LENGTH);
        for(let i=0;i<loopLen; i++){
            items[i].value = "";
            amounts[i].value = "";
        }

    }

  }

  render(){

    return(<div>
        {this.state.currentState}
        <button onClick={this.addItem} className="btn waves-effect waves-light">
			<i className="material-icons">add</i></button>
        <button onClick={this.removeItem} className="btn waves-effect waves-light" >
			<i className="material-icons">remove</i></button>
        <button onClick={this.reset} className="btn waves-effect waves-light">
			<i className="material-icons">restore</i></button>
      </div>);
  }
}

function imgRemove(e){
    e.preventDefault();
    $(e.target).siblings("input[type=file]").val('');
    $(e.target).siblings("input[type=hidden]").val('True');
    e.target.src="";
}

function imgPreview(e){
    e.preventDefault();
    var img = $(e.target).siblings("img").first();
    var r = new FileReader();
    r.readAsDataURL(e.target.files[0]);
    r.onload = function(e){
      img.attr("src", this.result);
    }
}

function Step(props){
  const hasContent = ("content" in props);
  const text = hasContent? props.content: "";
  //const img = hasContent? props.content.img:"";
  //const inputName = "step-img-" + props.ord;
	const placeholder = "步骤"+String(props.ord+1);
/*
    <input type="file" name={inputName} className="hidden" onChange={imgPreview}/>
    <img src={img} width="200" height="200" name="step-img-preview" onClick={imgRemove}/>
    <input type="hidden" name="removeExistingImg" value="False" /> */

  return(<li className="row">
	  <div className="input-field col s12">
    <textarea name="post-step" className="materialize-textarea" defaultValue={text} placeholder={placeholder} required/>
	  </div>
  </li>);
}

class Steplist extends React.Component {
  constructor(props){
    super(props);
    const hasContent = "content" in props;
    const l=[];
    if(hasContent){
      for(let i=0; i<props.content.length; i++){
        l.push(<Step content={props.content[i]} ord={i}/>)
      }
    }else{
      for(let i=0; i<DEFAULT_LIST_LENGTH; i++){
        l.push(<Step ord={i}/>)
      }
    }
    this.state={currentState: l, initialState: l, hasContent: hasContent};

    this.addStep = this.addStep.bind(this);
    this.removeStep = this.removeStep.bind(this);
    this.reset = this.reset.bind(this);
  }

  addStep(e){
    e.preventDefault();
    const currentState = this.state.currentState;
    const ord = currentState.length;
    const newState = currentState.concat([<Step ord={ord}/>]);
    this.setState({currentState: newState});
  }

  removeStep(e){
    e.preventDefault();
    const currentState = this.state.currentState;
    if(currentState.length <= 1) return;
    const newState = currentState.slice(0,-1);
    this.setState({currentState: newState});
  }

  reset(e){
    e.preventDefault();
    const initialState=this.state.initialState;
    this.setState({currentState: initialState});//只能恢复长度, 无法恢复Step组件里已经修改的部分
    //因此这里用jQuery重写回初始值
	//var img = $("[name=step-img-preview]");
    var text = $("[name=step-text]");
    //var input = $("[name^=step-img]");
    if(this.state.hasContent){
        var loopLen = Math.min(img.length, this.props.content.length);
        for(let i=0; i<loopLen; i++){
      //      img[i].src= this.props.content[i].img;
            text[i].value = this.props.content[i].text;
        //    input[i].value='';
        }
    }else{

        var loopLen = Math.min(img.length, DEFAULT_LIST_LENGTH);
        for(let i=0; i<loopLen; i++){
          //  img[i].src= "";
            text[i].value = "";
           // input[i].value='';
        }
    }
  }

  render(){
    return(<div>
        <ul>{this.state.currentState}</ul>
        <button className="btn waves-effect waves-light" onClick={this.addStep}>
			<i className="material-icons">add</i></button>
        <button className="btn waves-effect waves-light" onClick={this.removeStep}>
			<i className="material-icons">remove</i></button>
        <button className="btn waves-effect waves-light" onClick={this.reset}>
			<i className="material-icons">restore</i></button>
        </div>);
  }
}

function ItemRender(props){
    const element = props.content.map( e => (<tr><td>{e.item}</td><td>{e.amount}</td></tr>));
    return(<table><tbody>{element}</tbody></table>);
}

function StepRender(props){
    const element = props.content.map( e => (<li>
        <p>{e.text}</p><img src={e.img} width="200" height="200"/>
    </li>));

    return(<ol>{element}</ol>);
}

function QuestionRender(props){
    const element = props.content.map( q => (<div>
        <a href={q.creator_url}>{q.creator}</a>
        <p>{q.content}</p>
    </div>));

    return(<div>{element}</div>);
}

function confirmDelete(e){
    e.preventDefault();
    var decision = confirm("你确定要删除吗?");
    if(decision){
        window.location = e.target.dataset["url"];
    }else{
        return false;
    }

}

function RecipeManage(props){



    const element = props.content.map( r => (<li>
        <h4>{r.content.title}</h4>
        <img src={r.content.cover}/>
        <p>{r.content.intro}</p>
        <a href={r.urls.edit}>编辑</a>
        <a href="javascript:void(0);" data-url={r.urls.delete} onClick={confirmDelete}>删除</a>
    </li>));

    return(<ol>{element}</ol>);
}

function QuestionManage(props){
    const element = props.content.map( r => (<li>
        <a href={r.recipe_url}>{r.recipe_title}</a>
        <a href="javascript:void(0);" data-url={r.delete_url} onClick={confirmDelete}>删除</a>
        <p>{r.question_content}</p>
    </li>))

    return(<ol>{element}</ol>);
}

function RecipeRender(props){
    const element = props.recipes.map(r => (<li>
    <a href={r.url}>{r.title}</a>
    </li>));

    return(<ol>{element}</ol>);
}

/* vanillaJS follow / unfollow event */
async function follow(e){
	e.preventDefault();
	var element = e.currentTarget;
	//var username = $("a[data-user]").attr("data-user");
	var username = element.dataset.user;
	var url = "/user/follow/"+username;
	console.log(username);
	const response = await fetch(url, {
		method:"GET",
		mode:"same-origin",
		cache:"no-cache",
		credentials:"same-origin",
		headers:{"Content-Type":"application/json"},
		referer: "no-referer",
	});

	const result = await response.json();
	if(result["followed"]){
		element.classList.add("grey");
/*		var attr = element.getAttribute("class");
		attr = attr+" grey";
		element.setAttribute("class", attr)*/
		element.setAttribute("onclick", "unfollow(event);")
		M.toast({html:"关注成功!"});
	}else{
		M.toast({html:"关注失败!"});
	}
}

async function unfollow(e){
	e.preventDefault();
	var element = e.currentTarget;
	//var username = $("a[data-user]").attr("data-user");
	var username = element.dataset.user;
	console.log(username);
	var url = "/user/unfollow/"+username;

	const response = await fetch(url, {
		method:"GET",
		mode:"same-origin",
		cache:"no-cache",
		credentials:"same-origin",
		headers:{"Content-Type":"application/json"},
		referer: "no-referer",
	});

	const result = await response.json();
	if(result["unfollowed"]){
		/*
		var attr = element.getAttribute("class");
		var attrList = attr.split(" ");
		var greyPos = attrList.indexOf("grey");	
		attrList[greyPos]="";
		attr = attrList.reduce(function(a,b){return a+" "+b;});
		element.setAttribute("class", attr);*/
		element.classList.remove("grey");
		element.setAttribute("onclick", "follow(event);")
		M.toast({html:"取关成功!"});	
	}else{
		M.toast({html:"取关失败!"});	
	}

}

async function removeFollower(e){
	e.preventDefault();
	var element = e.currentTarget;
	// if set to e.target it would get data-user from the <i> element, which is undefined
	var username = element.dataset.user;
	var url = "/user/remove/"+username;
	console.log(username);
	const response =  await fetch(url, {
		method:"GET",
		mode:"same-origin",
		cache:"no-cache",
		credentials:"same-origin",
		headers:{"Content-Type":"application/json"},
		referer:"no-referer",
	});

	const result = await response.json();
	if(result["removed"]){
		element.classList.add("disabled");
		M.toast({html:"移除成功!"});
	}else{
		M.toast({html:"移除失败!"});
	}
}

/* add interaction for reply button */
function reply_fill(replyto){
	$("textarea[name=comment]").val("@"+replyto+" ").focus();
}

async function send_mail(e){
	e.preventDefault();
	const username = e.target.dataset.user;
	const url = e.target.dataset.url;

	const response = await fetch(url, {
		method:"GET",
		mode:"same-origin",
		cache:"no-cache",
		credentials:"same-origin",
		headers:{
			"Content-Type":"application/json",
			"X-Requested-With": "XMLHttpRequest"},
		referer:"no-referer",		
	});

	const result = await response.json();
	if(result["sent"]){
		M.toast({html: "确认邮件已重新发送到你的邮箱, 请于24小时内确认你的邮箱."});
	}else{
		M.toast({html: "很抱歉邮件未能正常发送, 请稍后重试."})
	}
}

