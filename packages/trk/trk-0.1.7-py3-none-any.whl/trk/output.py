import typer



def start_end_message(type, description, str_start, task, project, client, billable, str_end = None ,str_minutes = None ):

    if type == "start":
        prompt = "Started:"
    if type == "end":
        prompt = "Ended:"

    message_start = typer.style(prompt, fg = typer.colors.GREEN)
    message_event = typer.style(description, fg = typer.colors.BRIGHT_WHITE, bold = True)      
    first_line =  message_start + message_event 

   
    # task
    task_1 = typer.style("task: ",  fg = typer.colors.BRIGHT_YELLOW)
    task_2 = typer.style(task,  fg = typer.colors.WHITE)

    # project
    project_1 = typer.style("project: ",  fg = typer.colors.BRIGHT_YELLOW)
    project_2 = typer.style(project,  fg = typer.colors.WHITE)
    

    # client
    client_1 = typer.style("client: ",  fg = typer.colors.BRIGHT_YELLOW)
    client_2 = typer.style(client,  fg = typer.colors.WHITE)

    # billable
    billable_1 = typer.style("billable: ",  fg = typer.colors.BRIGHT_YELLOW)
    billable_2 = typer.style(billable,  fg = typer.colors.WHITE)

    if all(v is not None for v in [str_end, str_minutes]):
    # duration
        minutes = typer.style("minutes: ",  fg = typer.colors.BRIGHT_YELLOW)
        number = typer.style(str_minutes,  fg = typer.colors.WHITE)

        # time
        time_label = typer.style("time: ",  fg = typer.colors.BRIGHT_YELLOW)
        between = typer.style(" --> ", fg = typer.colors.BRIGHT_RED)
        start_time_1 = typer.style(str_start,  fg = typer.colors.WHITE)
        end_time_1 = typer.style(str_end,  fg = typer.colors.WHITE)

        typer.echo("\n" + first_line)
        typer.echo("\t" + time_label + start_time_1 + between + end_time_1)
        typer.echo("\t" + minutes + number)
        typer.echo("\t" + project_1 + project_2 )
        typer.echo("\t" + client_1 + client_2 + "\n")

    else:
    
        # time
        time_1 = typer.style("time: ",  fg = typer.colors.BRIGHT_YELLOW)
        time_2 = typer.style(str_start,  fg = typer.colors.WHITE)

        typer.echo("\n" + first_line)
        typer.echo("\t" + time_1 + time_2)
        typer.echo("\t" + task_1 + task_2 )
        typer.echo("\t" + project_1 + project_2 )
        typer.echo("\t" + client_1 + client_2 + "\n")