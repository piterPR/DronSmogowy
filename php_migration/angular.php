<?php if(isset($_POST['name'])): ?>
        <br/>
        Your name is <?php echo $_POST["name"]; ?>
        <?php $database_name = $_POST['name']; ?>
        <br/>
        <?php
            echo $database_name;
            $python = `python migration.py {$database_name}`;
            echo $python;
        ?>
<?php endif; ?>
