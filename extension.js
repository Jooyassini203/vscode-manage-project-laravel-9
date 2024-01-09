// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');
const { exec } = require('child_process');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
 
	console.log('Congratulations, your extension "manage-project-laravel-9" is now active!');
 
	let enclose_markers_lang = vscode.commands.registerCommand('manage-project-laravel-9.enclose-markers-lang', function () {
		
		const start_enclose = vscode.workspace.getConfiguration().get('start-enclose');
		const end_enclose = vscode.workspace.getConfiguration().get('end-enclose');

		const editor = vscode.window.activeTextEditor;
        if (editor) {
            const selection = editor.selection;
            const selectedText = editor.document.getText(selection);

            // Encadrer le texte sélectionné avec ***__ au début et __*** à la fin
            const newText = `${start_enclose}${selectedText}${end_enclose}`;

            // Remplacer le texte sélectionné par le nouveau texte encadré
            editor.edit(editBuilder => {
                editBuilder.replace(selection, newText);
            });
        }

	});
 

	let put_file_lang_foreach_view = vscode.commands.registerCommand('manage-project-laravel-9.put-file-lang-foreach-view', function () {
		const pythonCommand = 'python3'; 
		const pythonScript = 'scripts/put_file_lang.py';
		const actual_path = getCurrentWorkspacePath();
 
        if (actual_path) { 
            // Exécution de la commande Python
            exec(`${pythonCommand} ${pythonScript} ${actual_path}`, (error, stdout, stderr) => {
                if (error) { 
                    vscode.window.showErrorMessage(`Sortie du script Python : ${stdout}`)
                    return;
                }
    
                vscode.window.showInformationMessage(`Message : ${stdout}`)
            });
        }

	});


    


	context.subscriptions.push(enclose_markers_lang);
	context.subscriptions.push(put_file_lang_foreach_view);
}

function getCurrentWorkspacePath() {
    const workspaceFolders = vscode.workspace.workspaceFolders;
    
    if (workspaceFolders && workspaceFolders.length > 0) {
        // Retourne le premier répertoire de travail
        return workspaceFolders[0].uri.fsPath;
    } else {
        // Aucun répertoire de travail n'est ouvert
        return undefined;
    }
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
